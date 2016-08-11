<script>
    export default {
        data: function () {
            return {
                showRoles: false
            }
        },

        props: [
            'hide'
        ],

        events: {
            'end-selected': function (name) {
                if (name === this.hide) {
                    this.showRoles = true;
                }
            },
            'end-deselected': function (name) {
                if (name === this.hide) {
                    this.showRoles = false;
                }
            }
        }
    }
</script>

<style scoped>
    .test {
        background: red;
    }
</style>
