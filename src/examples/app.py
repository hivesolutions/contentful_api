#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Contentful API
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Contentful API.
#
# Hive Contentful API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Contentful API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Contentful API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import base

class ContentfulApp(appier.WebApp):

    def __init__(self, *args, **kwargs):
        appier.WebApp.__init__(
            self,
            name = "contentful",
            *args, **kwargs
        )

    @appier.route("/", "GET")
    def index(self):
        return self.entries()

    @appier.route("/entries", "GET")
    def entries(self):
        space = self.field("space")
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        entries = api.list_entries(space = space)
        return entries

    @appier.route("/entries/<str:id>", "GET")
    def entry(self, id):
        space = self.field("space")
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        entry = api.get_entry(id, space = space)
        return entry

    @appier.route("/content_types", "GET")
    def content_types(self):
        space = self.field("space")
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        content_types = api.list_content_types(space = space)
        return content_types

    @appier.route("/content_types/<str:id>", "GET")
    def content_type(self, id):
        space = self.field("space")
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        content_type = api.get_content_type(id, space = space)
        return content_type

    @appier.route("/assets", "GET")
    def assets(self):
        space = self.field("space")
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        assets = api.list_assets(space = space)
        return assets

    @appier.route("/assets/<str:id>", "GET")
    def asset(self, id):
        space = self.field("space")
        url = self.ensure_api()
        if url: return self.redirect(url)
        api = self.get_api()
        asset = api.get_asset(id, space = space)
        return asset

    @appier.route("/logout", "GET")
    def logout(self):
        return self.oauth_error(None)

    @appier.route("/oauth", "GET")
    def oauth(self):
        code = self.field("code")
        error = self.field("error")
        appier.verify(
            not error,
            message = "Invalid OAuth response (%s)" % error,
            exception = appier.OperationalError
        )
        api = self.get_api()
        access_token = api.oauth_access(code)
        self.session["ct.access_token"] = access_token
        return self.redirect(
            self.url_for("contentful.index")
        )

    @appier.exception_handler(appier.OAuthAccessError)
    def oauth_error(self, error):
        if "ct.access_token" in self.session: del self.session["ct.access_token"]
        return self.redirect(
            self.url_for("contentful.index")
        )

    def ensure_api(self):
        access_token = appier.conf("CONTENTFUL_TOKEN", None)
        access_token = self.session.get("ct.access_token", access_token)
        if access_token: return
        api = base.get_api()
        return api.oauth_authorize()

    def get_api(self):
        access_token = appier.conf("CONTENTFUL_TOKEN", None)
        access_token = self.session and self.session.get("ct.access_token", access_token)
        api = base.get_api()
        api.access_token = access_token
        return api

if __name__ == "__main__":
    app = ContentfulApp()
    app.serve()
else:
    __path__ = []
