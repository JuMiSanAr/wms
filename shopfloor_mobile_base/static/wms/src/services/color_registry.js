/**
 * Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
 * @author Simone Orsi <simahawk@gmail.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
import {utils_registry} from "./utils_registry.js";

export class ColorRegistry {
    // TODO: Add method to select the theme
    // to use for the app.
    // TODO: Investigate theme name (only "light" is recognized)
    constructor(theme, _default = "light") {
        this.themes = {};
        this.default_theme = _default;
    }

    add_theme(colors, theme) {
        if (_.isUndefined(theme)) theme = this.default_theme;
        this.themes[theme] = colors;
    }

    color_for(key, theme) {
        if (_.isUndefined(theme)) theme = this.default_theme;
        if (!this.themes[theme]) {
            console.log("Theme", theme, "not registered.");
            return null;
        }
        return this.themes[theme][key];
    }

    get_themes() {
        return this.themes;
    }
}

export var color_registry = new ColorRegistry();

utils_registry.add("colors", color_registry);

const error_color = "#c22a4a";
const success_color = "#8fbf44";
const accent_color = "#82B1FF";
const info_color = "#5e60ab";
const warning_color = "#e5ab00";
const todo_color = "#FFE3AC";

// TODO: search vuetify functions to reuse colors
// TODO: to check if scss is better option to registed themes
color_registry.add_theme(
    {
        /**
         * Standard keys
         */
        primary: "#491966",
        secondary: "#CFD2FF",
        accent: accent_color,
        error: error_color,
        info: info_color,
        success: success_color,
        // Warning: "#FFC107",
        warning: warning_color,
        /**
         * App specific
         */
        content_bg: "grey lighten-3",
        screen_step_done: success_color,
        screen_step_todo: todo_color,
        /**
         * Icons
         */
        info_icon: "info darken-2",
        /**
         * Buttons / actions
         */
        btn_action: "primary lighten-2",
        btn_action_cancel: "error",
        btn_action_warn: "warning",
        btn_action_complete: "success",
        btn_action_todo: "screen_step_todo",
        btn_action_back: "info lighten-1",
        /**
         * Selection
         */
        item_selected: "success",
        /**
         * Spinner
         */
        spinner: "dark_green",
        /**
         * Details
         */
        detail_main_card: "info lighten-4",
    },
    "dark"
); // TODO: we should bave a theme named "coosa" and select it

const dark_green = "#45763a";
const light_green = "#79b16d";

color_registry.add_theme(
    {
        /**
         * Standard keys
         */
        primary: dark_green,
        secondary: light_green,
        accent: accent_color,
        error: error_color,
        info: info_color,
        success: success_color,
        warning: warning_color,
        /**
         * App specific
         */
        content_bg: "grey lighten-3",
        screen_step_done: success_color,
        screen_step_todo: todo_color,
        /**
         * Icons
         */
        info_icon: info_color,
        /**
         * Buttons / actions
         */
        btn_action: dark_green,
        btn_action_cancel: error_color,
        btn_action_warn: warning_color,
        btn_action_complete: success_color,
        btn_action_todo: todo_color,
        btn_action_back: light_green,
        /**
         * Selection
         */
        item_selected: success_color,
        /**
         * Spinner
         */
        spinner: dark_green,
        /**
         * Details
         */
        detail_main_card: light_green,
    },
    "light"
);
