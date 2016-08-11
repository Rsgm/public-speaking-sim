<template>
    <div @click="click" :class="{selected: selected, deselected: !selected}">
        <h4>{{* choice.name }}</h4>
        <p>{{* choice.description }}</p>

        <ul class="uk-list" v-if="choice.list">
            <li v-for="li in choice.list">{{* li }}</li>
        </ul>
    </div>
</template>

<script>
    export default {
        data: function () {
            return {
                selected: false
            }
        },

        props: ['choice', 'radio'],

        methods: {
            click: function () {
                this.selected = true;
                this.$dispatch('select', this.choice.id);
            }
        },

        events: {
            'deselect-others': function (choice) {
                this.selected = this.choice.id === choice;
            },
            'deselect': function (choice) {
                if (this.choice.id === choice) {
                    this.selected = false;
                }
            }
        }
    }
</script>
