from flask import Flask, request, make_response, abort
from data import Data
from context import Context

ctx = Context()
data = Data(ctx)

app = Flask(__name__)

@app.route('/version')
def version(): return {"version": ctx.version}

@app.route('/search')
def search():
    q = request.args.get('q')
    if q == None: abort(404)
    n = request.args.get('n', ctx.annotation_limit, type=int)
    if n < 1 or n > ctx.annotation_limit: abort(404)
    distance = request.args.get('distance', ctx.cosine_distance, type=float)
    if distance < 0.0 or distance > 2.0: abort(404) 
    (n,items) = data.search(q, n, distance)
    return items

if __name__ == '__main__':
    app.run(host=ctx.server_ip, debug=ctx.debug, port=ctx.server_port)