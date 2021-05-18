import asyncio

from .datapools import RecyclableIterableDataPool

from mite_http import mite_http


@mite_http
async def get_homepage(ctx):
    async with ctx.transaction("Get homepage"):
        await ctx.http.get(ctx.config.get("url"))


@mite_http
async def post_form(ctx, name):
    async with ctx.transaction("Post form"):
        await ctx.http.post(
            ctx.config.get("url") + "/formsubmit",
            data=b"name=" + str(name).encode("utf-8"),
        )


names_file = open("mite/names.txt", "r")
datapool = RecyclableIterableDataPool([(name.strip(),) for name in names_file])


volumemodel = lambda start, end: 10


def scenario():
    return [
        ["mite.sws:get_homepage", None, volumemodel],
        ["mite.sws:post_form", datapool, volumemodel],
    ]
