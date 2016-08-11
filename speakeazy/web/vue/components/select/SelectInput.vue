<template>
    <div>
        <select-choice v-for="choice in choices" :choice="choice"></select-choice>
        <select-choice v-if="end" class="end" :choice="end"></select-choice>

        <input type="hidden" name="{{* name }}" v-model="selected" required="{{* required }}">
    </div>
</template>

<script>
    import SelectChoice from './SelectChoice.vue'

    export default {
        data: function () {
            return {
                selected: []
            }
        },

        props: [
            'id',
            'name',
            'choices', // in json form
            'multiple', // single or multiple select
            'required',
            'end'
        ],

        events: {
            'select': function (choice) {
                if (!this.multiple) {
                    this.selected = choice;
                    this.$broadcast('deselect-others', choice);
                } else if (this.selected.indexOf(choice) === -1) {
                    this.selected.push(choice);
                } else {
                    this.selected.$remove(choice);
                    this.$broadcast('deselect', choice);
                }

                if (this.end) {
                    var event = this.end.id === choice ? 'end-selected' : 'end-deselected';
                    this.$dispatch(event, this.name)
                }
            }
        },

        components: {
            'select-choice': SelectChoice
        }
    }
</script>
