# -*- coding: utf-8 -*-
import random

import odoo.addons.website_blog.controllers.main as main
import werkzeug
from odoo.addons.website.models.website import slug
from datetime import datetime

from odoo import http
from odoo.http import request

word_list = [
    'Duis', 'Proin', 'faucibus,', 'Pellentesque', 'at', 'lectus', 'fermentum', 'vel.', 'justo,', 'metus',
    'ultricies', 'mattis', 'mauris', 'mi.', 'facilisi.', 'Curabitur', 'sem', 'congue.', 'nibh,', 'dui', 'dolor',
    'molestie', 'gravida', 'sit', 'auctor', 'ut.', 'condimentum', 'Vestibulum', 'lacinia', 'consectetur.',
    'commodo,', 'massa', 'nulla', 'feugiat', 'convallis,', 'euismod', 'nibh.', 'nisl,', 'vel', 'congue', 'commodo',
    'velit.', 'turpis', 'nisl', 'dignissim', 'porta', 'Praesent', 'eget,', 'enim', 'ante.', 'iaculis.', 'neque',
    'velit', 'ante', 'hendrerit,', 'Ut', 'metus,', 'blandit', 'convallis', 'mollis', 'pulvinar', 'rutrum', 'Fusce',
    'tempor.', 'risus,', 'malesuada.', 'elit.', 'efficitur', 'urna', 'leo', 'dui.', 'elit', 'Morbi', 'consequat',
    'eros', 'quam.', 'nec', 'sed', 'facilisis', 'fringilla.', 'pellentesque', 'Nullam', 'eleifend', 'tincidunt,',
    'lacus', 'adipiscing', 'Suspendisse', 'in', 'lorem', 'et.', 'purus,', 'commodo.', 'placerat', 'egestas',
    'tempor', 'sollicitudin,', 'cursus', 'nulla.', 'Integer', 'porttitor', 'eu.', 'volutpat,', 'Cras',
    'consectetur', 'augue', 'primis', 'ex', 'posuere', 'laoreet.', 'Etiam', 'interdum', 'ut', 'Sed', 'urna.',
    'mi', 'a,', 'erat.', 'lorem.', 'neque.', 'Donec', 'tellus,', 'Phasellus', 'eget', 'cubilia', 'volutpat',
    'libero', 'rutrum,', 'mauris.', 'sodales', 'elit,', 'viverra', 'neque,', 'vitae,', 'felis', 'risus.', 'magna',
    'Quisque', 'felis,', 'sed.', 'pretium', 'sem.', 'mi,', 'aliquet.', 'scelerisque', 'hendrerit', 'faucibus',
    'Nulla', 'vulputate', 'lobortis', 'nulla,', 'viverra.', 'libero.', 'lobortis,', 'nec,', 'enim,', 'augue.',
    'Nam', 'ullamcorper', 'erat', 'sollicitudin', 'tincidunt', 'ac', 'Maecenas', 'molestie,', 'varius', 'lacus.',
    'orci', 'bibendum', 'pharetra', 'maximus', 'risus', 'lobortis.', 'Aenean', 'malesuada', 'tortor.', 'purus',
    'luctus', 'nisi', 'tellus.', 'Vivamus', 'pellentesque.', 'in,', 'Lorem', 'quis', 'amet,', 'a', 'tellus', 'id',
    'In', 'aliquet', 'justo', 'ligula.', 'cursus.', 'et', 'fringilla', 'eleifend,', 'vehicula', 'ipsum',
    'condimentum.', 'eu', 'ante,', 'non', 'suscipit', 'massa,', 'interdum,', 'iaculis', 'nibh', 'faucibus.', 'leo.',
    'auctor,', 'vitae', 'arcu.', 'vestibulum', 'varius.', 'diam,', 'ligula', 'tristique', 'in.', 'tortor', 'quam',
    'finibus.', 'arcu', 'Mauris', 'semper.', 'sapien', 'sagittis', 'dapibus', 'vulputate,', 'Aliquam', 'id.',
    'ultrices', 'Curae;', 'est', 'laoreet', 'amet', 'quis,', 'lectus.', 'rhoncus', 'accumsan', 'quam,', 'est.'
]


class IpSum:
    @staticmethod
    def generate_sentence(word_count=5):
        if word_count <= 0:
            raise Exception("Cannot make a sentence with zero words.")
        index = 0
        sentence = ''
        while index < word_count:
            sentence += ' ' + random.choice(word_list)
            index += 1
        return sentence[1:]


def gen_datetime(min_year=1900, max_year=datetime.now().year):
    start = datetime.today().replace(year=min_year, day=1, month=1).toordinal()
    end = datetime.today().replace(year=max_year).toordinal()
    return datetime.fromordinal(random.randint(start, end))


class WebsiteBlog(main.WebsiteBlog):
    @http.route('/blog/duplicate-blog-post', type='http', auth="public", website=True, methods=['POST'])
    def duplicate_blog_post(self, blog_post_id, post_count, title_words_count, starting_year):
        """ Replicate a blog post_count times.

        :param blog_post_id: id of the blog post currently browsed.
        :param post_count: how many times blog_post_id will be replicated.
        :param title_words_count: how many words the random title will have.
        :param starting_year: the publish date from blog posts where start from this year randomly.

        :return redirect to the last blog post created edition
        """

        attachments = request.env['ir.attachment'].search(
            [('url', 'not like', 'snippets'), ('public', '=', True), ('type', '=', 'url')])
        new_blog_post = None

        for i in range(int(post_count)):
            attachment = random.choice(attachments)
            new_blog_post = request.env['blog.post'].with_context(mail_create_nosubscribe=True).browse(
                int(blog_post_id)).copy({
                'name': IpSum.generate_sentence(int(title_words_count)),
                'subtitle': IpSum.generate_sentence(int(title_words_count) + 1),
                'website_published': True,
                'published_date': gen_datetime(int(starting_year)),
                'cover_properties': '{"background-image": "url(%s)", "resize_class": "cover container-fluid cover_full", "background-color": "oe_black", "opacity": "0.0"}' % attachment.url
            })
        return werkzeug.utils.redirect(
            "/blog/%s/post/%s?enable_editor=1" % (slug(new_blog_post.blog_id), slug(new_blog_post)))
