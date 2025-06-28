import customtkinter as ctk


class DropdownManager:
    active_dropdown = None
    _configure_bound = False

    @classmethod
    def set_active(cls, dropdown):
        if cls.active_dropdown is not None and cls.active_dropdown != dropdown:
            cls.active_dropdown._close_dropdown()
        cls.active_dropdown = dropdown

    @classmethod
    def close_all(cls):
        if cls.active_dropdown is not None:
            cls.active_dropdown._close_dropdown()
            cls.active_dropdown = None

    @classmethod
    def bind_configure(cls, toplevel):
        # Only bind once per window
        if not getattr(toplevel, "_dropdown_configure_bound", False):
            toplevel.bind("<Configure>", cls.on_window_configure)
            toplevel._dropdown_configure_bound = True

    @classmethod
    def on_window_configure(cls, event):
        # Only move the menu of the currently active dropdown
        if cls.active_dropdown is not None:
            cls.active_dropdown._move_menu()


class CustomDropdown:
    """Reusable custom dropdown class that can be used for any field"""

    def __init__(self, parent, parent_frame, row, column, options,
                 width=250, height=30, placeholder="-Select-", add_new_text="",
                 add_new_option=False, add_new_callback=None,
                 padx=(0, 20), pady=10,
                 entry_name=None, default_value=None, multiselect=False):

        self.parent = parent
        self.options = [str(opt) for opt in options]
        self.add_new_text = add_new_text
        self.add_new_option = add_new_option
        self.add_new_callback = add_new_callback
        self.width = width
        self.height = height
        self.placeholder = placeholder
        self.multiselect = multiselect

        # Maximum visible options before scrolling
        self.max_visible_options = 6  # Default value

        # Create variables
        self.selected_value = ctk.StringVar()
        self.selected_values = set()  # Set for multiselect
        self.selecting_option = False
        self.hovered_index = 0  # Track which option is hovered

        # Add search-related attributes
        self.search_text = ""
        self.filtered_options = [str(opt) for opt in options]

        # Container frame
        self.dropdown_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        self.dropdown_frame.grid(row=row, column=column, sticky="w", padx=padx, pady=pady)

        # Button that serves as the dropdown toggle
        self.dropdown_button = ctk.CTkButton(
            self.dropdown_frame, text=placeholder,
            width=width, height=height,
            fg_color=parent.BG_COLOR_2, text_color=parent.TEXT_COLOR_ENTRY, hover_color="#D1E3FA",
            border_width=parent.BORDER_WIDTH, border_color=parent.BORDER_COLOR,
            anchor="w",
            command=self.show_dropdown
        )
        self.dropdown_button.pack(fill="x")

        # Keep a reference in the parent's entries dict if requested
        if entry_name and hasattr(parent, 'entries'):
            if self.multiselect:
                parent.entries[entry_name] = self  # Store the whole object for multiselect
            else:
                parent.entries[entry_name] = self.selected_value

        # Add a window-level binding only once for all dropdowns
        toplevel = parent.winfo_toplevel()
        if not hasattr(toplevel, '_dropdown_focus_out_bound'):
            toplevel._dropdown_focus_out_bound = True
            toplevel.bind("<FocusOut>", self._handle_focus_out)

        # Bind keyboard events to the application
        toplevel.bind("<KeyPress>", self._handle_key_press, add="+")

        DropdownManager.bind_configure(toplevel)

        # Set default value if provided
        if default_value is not None:
            self.set(default_value)

    def _handle_focus_out(self, event):
        """Handle focus out event - must be an instance method to work properly"""
        # Only process if this dropdown is active
        if DropdownManager.active_dropdown != self:
            return

        if hasattr(self, 'menu') and self.menu.winfo_exists():
            # Get widget that received focus
            focused_widget = event.widget.focus_get()

            # Check if the newly focused widget is inside our dropdown
            if focused_widget:
                # Check if it's our search entry or inside our menu
                is_in_menu = str(focused_widget).startswith(str(self.menu))
                is_search = hasattr(self, 'search_entry') and focused_widget == self.search_entry

                if is_in_menu or is_search:
                    return

        # Add a small delay to allow for button clicks to process
        self.parent.after(100, DropdownManager.close_all)

    def _move_menu(self):
        # Move the dropdown menu (called only by active dropdown)
        if hasattr(self, 'menu') and self.menu.winfo_exists():
            x = self.dropdown_button.winfo_rootx()
            y = self.dropdown_button.winfo_rooty() + self.dropdown_button.winfo_height() + 2
            self.menu.geometry(f"+{x}+{y}")

    def _close_dropdown(self):
        """Close the dropdown menu - called by DropdownManager"""
        if hasattr(self, 'menu') and self.menu.winfo_exists():
            self.menu.destroy()

    def _update_hover(self, index):
        if not hasattr(self, "option_buttons"):
            return
        for i, btn in enumerate(self.option_buttons):
            if i == index:
                btn.configure(fg_color="#D1E3FA")

                # If using scrollable frame, ensure the hovered item is visible
                if hasattr(self, 'options_frame') and hasattr(self.options_frame, '_parent_canvas'):
                    # Calculate positions to make the item visible
                    option_height = 35  # Same as defined in show_dropdown
                    visible_area = self.options_frame._parent_canvas.winfo_height()

                    # Get current scroll position
                    current_scroll = self.options_frame._parent_canvas.yview()[0] * (
                            len(self.option_buttons) * option_height)

                    # Calculate position of hovered item
                    item_pos = index * option_height

                    # Check if item is outside visible area
                    if item_pos < current_scroll:
                        # Scroll up to show item
                        self.options_frame._parent_canvas.yview_moveto(
                            item_pos / (len(self.option_buttons) * option_height))
                    elif item_pos + option_height > current_scroll + visible_area:
                        # Scroll down to show item
                        new_pos = (item_pos + option_height - visible_area) / (len(self.option_buttons) * option_height)
                        self.options_frame._parent_canvas.yview_moveto(new_pos)
            else:
                btn.configure(fg_color=self.parent.BG_COLOR_2)
        self.hovered_index = index

    def show_dropdown(self):
        # Close any existing dropdown
        if hasattr(self, 'menu') and self.menu.winfo_exists():
            self.menu.destroy()
            return

        # Make sure to properly clean up any previous active dropdown
        if DropdownManager.active_dropdown is not None and DropdownManager.active_dropdown != self:
            DropdownManager.active_dropdown._close_dropdown()

        DropdownManager.set_active(self)

        # Reset any lingering keyboard focus issues
        toplevel = self.parent.winfo_toplevel()
        toplevel.focus_set()

        # Find the index of the currently selected value (if any)
        selected_value = self.selected_value.get()
        if selected_value and selected_value in self.options:
            self.hovered_index = self.options.index(selected_value)
        else:
            self.hovered_index = 0  # Default to first option if nothing selected

        # Create a toplevel window for dropdown
        self.menu = ctk.CTkToplevel(self.parent)
        self.menu.attributes("-topmost", True)
        self.menu.overrideredirect(True)

        # Calculate dimensions and position
        menu_width = self.width
        option_height = 35  # Height of each option
        option_padding = 5  # Padding for each option

        # Calculate total height needed
        options_count = len(self.options)
        visible_options = min(options_count, self.max_visible_options)

        # Determine if scrollbar is needed
        self.scrollbar_needed = options_count > self.max_visible_options

        # Calculate menu height with scrolling limit
        options_height = visible_options * option_height

        # Calculate menu height with proper spacing
        menu_height = options_height + option_padding * 2

        # Add additional space for "Add New" button if needed
        add_new_height = 45 if self.add_new_option else 0
        menu_height += add_new_height

        # Store potential search height for later
        self.search_height = 40

        x = self.dropdown_button.winfo_rootx()
        y = self.dropdown_button.winfo_rooty() + self.dropdown_button.winfo_height() + 5
        self.menu.geometry(f"{menu_width}x{menu_height + 5}+{x}+{y}") # +5 to ensure it fits

        # Store original dimensions for resizing when search appears
        self.original_menu_height = menu_height

        # Create frames
        outer_frame = ctk.CTkFrame(
            self.menu, fg_color="transparent", corner_radius=0,
            border_width=1, border_color=self.parent.BORDER_COLOR,
            width=menu_width, height=menu_height
        )
        outer_frame.pack(fill="both", expand=True)
        outer_frame.pack_propagate(False)

        # Main content frame
        self.menu_frame = ctk.CTkFrame(
            outer_frame, fg_color=self.parent.BG_COLOR_2, corner_radius=0, border_width=0,
            width=menu_width - 2, height=menu_height - 2
        )
        self.menu_frame.pack(fill="both", expand=True, padx=1, pady=2) # keep this at pady=2 to ensure border visibility
        self.menu_frame.pack_propagate(False)

        # Create search frame but keep it hidden initially
        self.search_frame = ctk.CTkFrame(self.menu_frame, fg_color=self.parent.BG_COLOR_2, corner_radius=0)
        self.search_entry = ctk.CTkEntry(
            self.search_frame, placeholder_text="Search...",
            width=menu_width - 20, height=30,
            fg_color="white",
            border_width=1, border_color=self.parent.BORDER_COLOR
        )
        self.search_entry.pack(padx=8, pady=5, fill="x")
        self.search_entry.bind("<KeyRelease>", self._filter_options)

        # Create main content area
        self.content_frame = ctk.CTkFrame(
            self.menu_frame,
            fg_color=self.parent.BG_COLOR_2,
            corner_radius=0,
            height=menu_height - 2
        )
        self.content_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # IMPORTANT: Pack the "Add New" button FIRST - this ensures it's at the bottom and always visible
        # Add "Add New" option if requested
        if self.add_new_option:
            self.add_item_frame = ctk.CTkFrame(
                self.content_frame,
                fg_color=self.parent.BG_COLOR_2,
                corner_radius=0,
                height=add_new_height
            )
            self.add_item_frame.pack(fill="x", side="bottom", pady=(5, 5))
            self.add_item_frame.pack_propagate(False)

            add_new = ctk.CTkButton(
                self.add_item_frame,
                text=f"+ Add New {self.add_new_text}",
                fg_color="#F6F6F6",
                text_color="#2563eb",
                hover_color="#D1E3FA",
                height=36,
                corner_radius=5,
                command=self.handle_add_new
            )
            add_new.pack(fill="both", expand=True, padx=5, pady=5)

        # Create options frame AFTER the add new button (so it's positioned above it)
        options_container = ctk.CTkFrame(
            self.content_frame,
            fg_color=self.parent.BG_COLOR_2,
            corner_radius=0
        )
        options_container.pack(fill="both", expand=True)

        # Create options frame as a scrollable frame with scrollbar hidden when not needed
        self.options_frame = ctk.CTkScrollableFrame(
            options_container,
            fg_color=self.parent.BG_COLOR_2,
            corner_radius=0,
            width=menu_width - 5 if self.scrollbar_needed else menu_width,  # Adjust width if scrollbar is visible
            height=options_height - (add_new_height if self.add_new_option else 0),  # Subtract space for add_new button
            scrollbar_button_color="#D1E3FA",
            scrollbar_button_hover_color="#2563eb"
        )
        self.options_frame.pack(fill="both", expand=True)

        # Hide scrollbar if not needed
        if not self.scrollbar_needed:
            if hasattr(self.options_frame, "_scrollbar"):
                self.options_frame._scrollbar.grid_remove()

        # Initialize filtered options and display them
        self.filtered_options = self.options.copy()
        self.option_buttons = []
        self._update_displayed_options()

    def _handle_key_press(self, event):
        """Handle keyboard input when dropdown is open"""
        # Only process keypresses if this dropdown is active
        if DropdownManager.active_dropdown != self:
            return

        # If dropdown is not open, ignore
        if not hasattr(self, 'menu') or not self.menu.winfo_exists():
            return

        # Show search frame if it's hidden and the key is a character
        if len(event.char) == 1 and event.char.isprintable():
            if not self.search_frame.winfo_ismapped():
                # First pack the search frame at the top
                self.search_frame.pack(fill="x", pady=(5, 5), side="top", in_=self.menu_frame,
                                       before=self.content_frame)

                # Resize the menu to accommodate the search bar
                new_height = self.original_menu_height + self.search_height

                # Get current position
                x = self.menu.winfo_x()
                y = self.menu.winfo_y()

                # Update geometry
                self.menu.geometry(f"{self.width}x{new_height}+{x}+{y}")

            # Set focus and insert character (whether visible or not)
            self.search_entry.delete(0, "end")
            self.search_entry.insert(0, event.char)

            # Explicitly set focus and update active dropdown
            self.search_entry.focus_set()
            DropdownManager.set_active(self)

            self._filter_options(None)

        # Handle navigation keys
        elif event.keysym == 'Escape':
            self._close_dropdown()
        elif event.keysym == 'Return' and self.filtered_options:
            if 0 <= self.hovered_index < len(self.filtered_options):
                self.select_option(self.filtered_options[self.hovered_index])
        elif event.keysym == 'Down':
            self._navigate_options(1)
        elif event.keysym == 'Up':
            self._navigate_options(-1)

    def _filter_options(self, event=None):
        """Filter options based on search text"""
        if hasattr(self, "search_entry"):
            search_text = self.search_entry.get().lower()

            # If search text is empty, remove search bar and resize back to original
            if not search_text:
                if self.search_frame.winfo_ismapped():
                    # Hide search frame
                    self.search_frame.pack_forget()

                    # Resize back to original size
                    x = self.menu.winfo_x()
                    y = self.menu.winfo_y()
                    self.menu.geometry(f"{self.width}x{self.original_menu_height}+{x}+{y}")

                    # Important: Reset focus to the toplevel window to ensure key events work again
                    toplevel = self.parent.winfo_toplevel()
                    toplevel.focus_set()

                    # Make sure this dropdown stays active
                    DropdownManager.set_active(self)

            # Update filtered options
            self.filtered_options = [opt for opt in self.options if search_text in opt.lower()]

            # Update scrollbar visibility based on the number of filtered options
            if hasattr(self, 'options_frame') and hasattr(self.options_frame, '_scrollbar'):
                if len(self.filtered_options) > self.max_visible_options:
                    # Show scrollbar
                    self.options_frame._scrollbar.grid()
                else:
                    # Hide scrollbar
                    self.options_frame._scrollbar.grid_remove()

            self._update_displayed_options()

    def _update_displayed_options(self):
        """Update the displayed options based on filtering"""
        # Clear existing options
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        self.option_buttons = []
        self.checkboxes = [] if self.multiselect else None

        if not self.filtered_options:
            # Show "No results" message
            no_results_frame = ctk.CTkFrame(
                self.options_frame, fg_color=self.parent.BG_COLOR_2, corner_radius=0, height=35
            )
            no_results_frame.pack(fill="x", pady=(5, 0))
            no_results_frame.pack_propagate(False)

            ctk.CTkLabel(
                no_results_frame, text="No matches found",
                text_color="gray"
            ).pack(pady=10)
            return

        # Reset hovered index if needed
        if self.hovered_index >= len(self.filtered_options):
            self.hovered_index = 0

        # Update scrollbar visibility based on number of options
        if hasattr(self, 'options_frame'):
            needs_scrollbar = len(self.filtered_options) > self.max_visible_options

            if hasattr(self.options_frame, "_scrollbar"):
                if needs_scrollbar:
                    self.options_frame._scrollbar.grid()
                else:
                    self.options_frame._scrollbar.grid_remove()

        # Add filtered options
        for i, option in enumerate(self.filtered_options):
            item_frame = ctk.CTkFrame(
                self.options_frame, fg_color=self.parent.BG_COLOR_2, corner_radius=0, height=35
            )
            item_frame.pack(fill="x", pady=0)
            item_frame.pack_propagate(False)

            if self.multiselect:
                # Create a row with checkbox and label
                check_var = ctk.BooleanVar(value=option in self.selected_values)
                checkbox = ctk.CTkCheckBox(
                    item_frame, text=f"{option}",
                    variable=check_var,
                    fg_color="#2563eb",
                    hover_color="#1E40AF",
                    text_color="black",
                    checkbox_width=20, checkbox_height=20,
                    border_width=1, border_color=self.parent.BORDER_COLOR,
                    corner_radius=0,
                    command=lambda opt=option, var=check_var: self.toggle_option(opt, var.get())
                )
                checkbox.pack(fill="x", padx=5, pady=5, anchor="w")
                self.checkboxes.append((checkbox, check_var))

                # Mouse events for hover effect
                item_frame.bind("<Enter>", lambda e, idx=i: self._update_hover(idx))
                item_frame.bind("<Leave>", lambda e: self._update_hover(self.hovered_index))

            else:
                # Standard button for single selection
                option_btn = ctk.CTkButton(
                    item_frame, text=f"  {option}",
                    fg_color="#D1E3FA" if i == self.hovered_index else self.parent.BG_COLOR_2,
                    text_color="black", text_color_disabled="black", hover_color="#D1E3FA",
                    height=35, anchor="w", corner_radius=5,
                    command=lambda opt=option: self.select_option(opt)
                )
                option_btn.pack(fill="both", expand=True, padx=(5, 5), pady=(5, 0))

                # Mouse events
                option_btn.bind("<Enter>", lambda e, idx=i: self._update_hover(idx))
                option_btn.bind("<Leave>", lambda e: self._update_hover(self.hovered_index))

                self.option_buttons.append(option_btn)

    def toggle_option(self, option, checked):
        """Toggle an option in multiselect mode"""
        if checked:
            self.selected_values.add(option)
        else:
            self.selected_values.discard(option)

        # Update dropdown button text
        self.update_button_text()

        # Reset focus to toplevel and ensure this dropdown remains active
        toplevel = self.parent.winfo_toplevel()
        toplevel.focus_set()
        DropdownManager.set_active(self)

    def update_button_text(self):
        """Update the dropdown button text based on selected options"""
        if not self.multiselect:
            if self.selected_value.get():
                self.dropdown_button.configure(text=self.selected_value.get(), text_color="black")
            else:
                self.dropdown_button.configure(text=self.placeholder, text_color=self.parent.TEXT_COLOR_ENTRY)
            return

        if not self.selected_values:
            self.dropdown_button.configure(text=self.placeholder, text_color=self.parent.TEXT_COLOR_ENTRY)
        elif len(self.selected_values) == 1:
            self.dropdown_button.configure(text=next(iter(self.selected_values)), text_color="black")
        elif len(self.selected_values) <= 2:
            # Show all selected values if there are only a few
            text = ", ".join(self.selected_values)
            self.dropdown_button.configure(text=text, text_color="black")
        else:
            # Show count if there are many
            text = f"{len(self.selected_values)} items selected"
            self.dropdown_button.configure(text=text, text_color="black")

    def _navigate_options(self, direction):
        """Navigate through options with keyboard"""
        if not self.filtered_options:
            return

        new_index = self.hovered_index + direction
        if new_index < 0:
            new_index = len(self.filtered_options) - 1
        elif new_index >= len(self.filtered_options):
            new_index = 0

        self._update_hover(new_index)

    def select_option(self, option):
        if self.multiselect:
            # In multiselect mode, toggle the option
            if option in self.selected_values:
                self.selected_values.discard(option)
            else:
                self.selected_values.add(option)
            self.update_button_text()
        else:
            # Single select mode
            self.selecting_option = True
            self.selected_value.set(option)
            self.dropdown_button.configure(text=option, text_color="black")
            self.parent.update()

            # Close dropdown
            if hasattr(self, 'menu') and self.menu.winfo_exists():
                self.menu.destroy()
            # Clear active dropdown
            DropdownManager.active_dropdown = None
            self.selecting_option = False

    def handle_add_new(self):
        # Close dropdown first
        if hasattr(self, 'menu') and self.menu.winfo_exists():
            self.menu.destroy()
        # Clear active dropdown
        DropdownManager.active_dropdown = None
        # Call callback if provided
        if self.add_new_callback:
            self.add_new_callback()

    def get_selected_values(self):
        """Get all selected values for multiselect mode"""
        return self.selected_values

    def get(self):
        """Get the currently selected value or values."""
        if self.multiselect:
            return list(self.get_selected_values())
        return self.selected_value.get()

    def set(self, value):
        """Set the dropdown to specific value(s)."""
        if self.multiselect:
            if isinstance(value, (list, set, tuple)):
                self.selected_values = {v for v in value if v in self.options}
            elif value in self.options:
                self.selected_values = {value}
            else:
                self.selected_values = set()
            self.update_button_text()
        else:
            if value in self.options:
                self.selected_value.set(value)
                self.dropdown_button.configure(text=value, text_color="black")
            else:
                self.selected_value.set("")
                self.dropdown_button.configure(text=self.placeholder, text_color=self.parent.TEXT_COLOR_ENTRY)

    def set_options(self, options):
        """Update the dropdown options and refresh the button text/selection if needed."""
        self.options = [str(opt) for opt in options]
        self.filtered_options = self.options.copy()
        # If the current value is not in the new options, clear it
        if not self.multiselect:
            if self.selected_value.get() not in self.options:
                self.selected_value.set("")
                self.dropdown_button.configure(text=self.placeholder, text_color=self.parent.TEXT_COLOR_ENTRY)
            else:
                self.dropdown_button.configure(text=self.selected_value.get(), text_color="black")
        else:
            self.selected_values = {v for v in self.selected_values if v in self.options}
            self.update_button_text()

