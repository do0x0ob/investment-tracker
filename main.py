import asyncio
from utils import *

# use these code if run in jupyternotebook
# if 'IPKernelApp' in get_ipython().config:
#     import nest_asyncio
#     nest_asyncio.apply()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main(0))
