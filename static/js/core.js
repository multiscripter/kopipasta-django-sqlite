$(function() {
    $( "#cat-menu" ).selectmenu();

    var pastaLoader = {
        body: null,
        catBox: null,
        p_head: null,
        p_body: null,
        buttons: false,

        getPhrase: function(params) {
            var self = this;
            url = window.location.origin;
            if (params)
                url += '?' + params;
            $.ajax({
                url: url,
                headers: { 'ACCEPT': 'application/json' }
            }).done(function(data) {
                if (data) {
                    if (data.hasOwnProperty('item')) {
                        self.p_head.data('id', data.item.id);
                        self.p_head.text(data.item.title);
                        self.p_body.text(data.item.text);
                    }
                    if (data.hasOwnProperty('pos')) {
                        self.buttons.removeClass('disabled');
                        if (data.pos == 'first')
                            self.buttons.eq(0).addClass('disabled');
                        else if (data.pos == 'last')
                            self.buttons.eq(2).addClass('disabled');
                    }
                }
            });
        },

        requestByCategory: function(value) {
            var params = 'action=first';
            if (parseInt(value) > 0)
                params = '&category_id=' + value;
            this.getPhrase(params);
        },

        requestByAction: function(action) {
            var params = ['current_id=' + this.p_head.data('id')];
            if (action == 'prev' || action == 'next')
                params.push('action=' + action);
            var cat = this.catBox.find('input:checked').val();
            if (cat && 0 < cat)
                params.push('category_id=' + cat);
            params = params.join('&');
            this.getPhrase(params);
        },

        init: function() {
            this.body = $('body');
            this.catBox = $('#cat-box');
            this.p_head = $('#pasta-head');
            this.p_body = $('#pasta-body');
            this.buttons = $('#buttons .btn');

            var self = this;
            this.body.on('selectmenuselect', function(event, ui) {
                self.requestByCategory(event.target.value);
            });

            if (this.buttons.length) {
                this.buttons.each(function() {
                    $(this).on('click', function(event) {
                        event.preventDefault();
                        action = $(this).attr('href').split('=')[1];
                        self.requestByAction.call(self, action);
                    });
                });
            }
        }
    }
    pastaLoader.init();
});