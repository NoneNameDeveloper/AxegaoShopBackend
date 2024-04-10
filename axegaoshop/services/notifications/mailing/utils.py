def render_template(template, **kwargs):
    """ renders a Jinja template into HTML """

    import jinja2
    templateLoader = jinja2.FileSystemLoader(searchpath="axegaoshop/services/notifications/mailing/templates/")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templ = templateEnv.get_template(template)
    return templ.render(**kwargs)

