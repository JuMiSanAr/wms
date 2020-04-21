/* eslint-disable strict */
Vue.component("manual-select", {
    props: {
        records: {
            type: Array,
            default: [],
        },
        grouped_records: {
            type: Array,
            default: function() {
                return [];
            },
        },
        key_title: {
            type: String,
            default: "name",
        },
        options: {
            type: Object,
        },
        list_item_fields: {
            type: Array,
            default: function() {
                return [];
            },
        },
    },
    data: function() {
        return {
            selected: null,
        };
    },
    created() {
        // Relies on properties
        this.selected = this._initSelected();
    },
    methods: {
        _initSelected() {
            const initValue = this.opts.initValue;
            let selected = false;
            if (this.opts.multiple) {
                selected = initValue ? [initValue] : [];
                if (this.opts.initSelectAll) {
                    selected = [];
                    _.each(this.records, function(rec, index) {
                        selected.push(rec.id);
                    });
                }
            } else {
                selected = initValue ? initValue : false;
            }
            return selected;
        },
        _getSelected() {
            const self = this;
            let selected_records = null;
            if (this.opts.multiple) {
                selected_records = _.filter(
                    self.records, function(o) { return _.has(self.selected, o.id); }
                );
            } else {
                selected_records = _.head(_.filter(
                    self.records, function(o) { return self.selected === o.id; }
                ));
            }
            console.log("SELECTED", selected_records);
            return selected_records
        },
        handleSelect() {
            if(!this.opts.showActions){
                this.$root.trigger('select', this._getSelected())
            }
        },
        handleAction(action) {
            this.$root.trigger('select', this._getSelected())
        },
    },
    computed: {
        has_records() {
            return this.records.length > 0;
        },
        opts() {
            // Defining defaults for an Object property
            // works only if you don't pass the property at all.
            // If you pass only one key, you'll lose all defaults.
            const opts = _.defaults({}, this.$props.options, {
                bubbleUpAction: false,
                showActions: true,
                initSelectAll: false,
                initValue: null,
                multiple: false,
                showCounters: false,
                list_item_component: "list-item",
                list_item_extra_component: "",
            });
            return opts;
        },
        list_item_options() {
            return {
                key_title: this.key_title,
                showCounters: this.opts.showCounters,
                fields: this.opts.list_item_fields,
            };
        },
        selectable() {
            if (!this.grouped_records.length) {
                // Simulate grouping (allows to keep template the same)
                return [{key: "no-group", title: "", records: this.records}];
            }
            return this.grouped_records;
        },
        klass() {
            const bits = ["manual-select"];
            _.forEach(this.opts, function(v, k) {
                if (v) {
                    let bit = "with-" + k;
                    if (typeof v === "string") {
                        bit += "--" + v;
                    }
                    bits.push(bit);
                }
            });
            return bits.join(" ");
        },
    },
    template: `
    <div :class="klass">
        <v-card outlined>
            <v-list v-if="has_records">
                <div class="select-group" v-for="(group, gindex) in selectable" :key="gindex">
                    <v-card-title v-if="group.title">{{ group.title }}</v-card-title>
                    <div class="list-item-wrapper" v-for="(rec, index) in group.records"">
                        <v-list-item :key="gindex + '-' + index">
                            <v-list-item-content>
                                <component
                                    :is="opts.list_item_component"
                                    :options="list_item_options"
                                    :record="rec"
                                    :index="index"
                                    :count="group.records.length"
                                    />
                            </v-list-item-content>
                            <v-list-item-action>
                                <v-checkbox
                                    v-model="selected"
                                    :input-value="rec.id"
                                    :true-value="rec.id"
                                    :value="rec.id"
                                    @change="handleSelect()"
                                    ></v-checkbox>
                            </v-list-item-action>
                        </v-list-item>
                        <div class="extra" v-if="opts.list_item_extra_component">
                            <component
                                :is="opts.list_item_extra_component"
                                :options="list_item_options"
                                :record="rec"
                                :index="index"
                                :count="group.records.length"
                                />
                        </div>
                    </div>
                </div>
            </v-list>
            <v-alert tile type="error" v-if="!has_records">
                No record found.
            </v-alert>
        </v-card>
        <v-row class="actions bottom-actions" v-if="has_records && opts.showActions">
            <v-col>
                <v-btn depressed color="success" @click="handleAction('submit')">
                    Start
                </v-btn>
            </v-col>
            <v-col>
                <v-btn depressed color="default" @click="$root.trigger('back')" class="float-right">
                    Back
                </v-btn>
            </v-col>
        </v-row>
    </div>
  `,
});
