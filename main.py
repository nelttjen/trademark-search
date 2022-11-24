from Site import app, api
from Site.update_cookie import update_cookie
from Api import routes, APIROUTE


if __name__ == '__main__':
    api.add_resource(routes.TrademarkSearch, APIROUTE + '/search/')
    api.add_resource(routes.TrademarkInfo, APIROUTE + '/trademark/')
    update_cookie()
    app.run('0.0.0.0', 8080)