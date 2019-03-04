odoo.define('blog_tools.navbar', function (require) {
    "use strict";

    const Dialog = require('web.Dialog'),
        core = require('web.core'),
        Widget = require('web.Widget'),
        ajax = require('web.ajax'),
        qweb = core.qweb,
        _t = core._t;

    const DuplicateBlogPost = Widget.extend({
        template: 'blog_tools.DuplicationLink',
        init: function () {
            this._super.apply(this, arguments);
        },
        start: function () {
            const self = this;
            this._openDialog.bind(self);
            this.$el.on('click', function (e) {
                self._openDialog(e);
            });
            this.dialog = new Dialog(this, {
                title: _t('Duplication Form'),
                $content: $(qweb.render('blog_tools.DuplicationForm', {
                    csrf_token: this.$el.parent().data('csrf-token'),
                    res_id: this.$el.parent().data('res-id'),
                    years: self._yearsList()
                })),
                size: 'medium',
                buttons: [
                    {
                        text: _t('Duplicate'),
                        classes: 'btn-primary',
                        close: true,
                        click: self._doReplication,
                    }
                ]
            })
        },
        _yearsList: function (bottom = 2000) {
            let first = new Date().getFullYear(),
                list = [];
            while (first > bottom) {
                list.push(first--);
            }
            return list;
        },
        _openDialog: function () {
            this.dialog.open();
        },
        _doReplication: function () {
            this.$content.find('.form-horizontal').submit();
        },
    });

    $(function () {
        ajax.loadXML('/blog_tools/static/src/xml/blog_tools_form.xml', qweb).then(function () {
            let duplicate = new DuplicateBlogPost(this);
            duplicate.appendTo($('li.blog-tool-duplication'));
        });
    });

    return {
        DuplicateBlogPost: DuplicateBlogPost,
    };
});