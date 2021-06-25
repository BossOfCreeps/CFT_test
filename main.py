from aiohttp.web import Application, run_app
from configargparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from views import LimitsView, TransferView

parser = ArgumentParser(auto_env_var_prefix='ANALYZER_', formatter_class=ArgumentDefaultsHelpFormatter)

parser.add_argument('--api-address', default='0.0.0.0', help='IPv4/IPv6 address API server would listen on')
parser.add_argument('--api-port', type=int, default=8001, help='TCP port API server would listen on')


def main():
    args = parser.parse_args()
    app = Application()
    app.router.add_route('*', '/limits', LimitsView)
    app.router.add_route('*', '/transfers', TransferView)
    run_app(app, host=args.api_address, port=args.api_port)


if __name__ == '__main__':
    main()
