import asyncio
import base64
from app.service.solver import PuzleSolver
from pyppeteer import launch
import app.service.emailutil as emailutil
import app.service.passwordutil as passwordutil
import time

cookie = {"name": "isShownWholeAnimation", "value": "1", "domain": "genshin.mihoyo.com", "path": "/",
          "expires": 208968028035, "size": 22, "httpOnly": False, "secure": False, "session": False
          }


async def generate_account():
    try:
        print("started")
        start = time.time()
        browser = await launch(
            ignoreHTTPSErrors=True, headless=True, handleSIGINT=False, handleSIGTERM=False, handleSIGHUP=False,
            args=["--no-sandbox"]
        )
        page = await browser.newPage()
        await page.setCookie(cookie)
        await page.setViewport({"width": 1366, "height": 768})
        await page.goto("https://genshin.mihoyo.com/en/home", options={"waitUntil": "networkidle2"})
        await page.click(".login__btn")
        await page.click(".to-register")
        await page.click("input[placeholder=Email]")

        mail = emailutil.generate()
        await page.keyboard.type(mail)
        await page.click(".input-inner-btn")
        code = emailutil.get_verification(mail)
        await page.click("input[placeholder='Verification Code']")
        await page.keyboard.type(code)
        await page.click("input[placeholder='Password cannot be only numbers (8-15 characters)']")

        passwrd = passwordutil.get_pass()
        await page.keyboard.type(passwrd)
        await page.click("input[placeholder='Confirm Password']")
        await page.keyboard.type(passwrd)
        await page.mouse.click(675, 554)
        await page.waitFor(5000)
        await page.screenshot({"path": "7.png"})
        slice = await page.querySelector(".geetest_canvas_slice")
        slice_64 = await page.evaluate("(slice) => slice.toDataURL('image/png').substring(21)", slice)
        slice_png = base64.b64decode(slice_64)
        bg = await page.querySelector(".geetest_canvas_bg")
        bg_64 = await page.evaluate("(bg) => bg.toDataURL('image/png').substring(21)", bg)
        bg_png = base64.b64decode(bg_64)

        solver = PuzleSolver(slice_png, bg_png)
        solution = solver.get_position()

        piece = await page.querySelector(".geetest_slider_button")
        box = await piece.boundingBox()
        await page.mouse.move(box.get("x") + box.get("width") / 2, box.get("y") + box.get("height") / 2)
        await page.mouse.down()

        await page.waitFor(2000)

        await page.mouse.move(
            box.get("x") + int(solution) + 32,
            box.get("y"), options={"steps": 10}
        )
        await page.mouse.up()
        await page.waitFor(3000)
        await browser.close()
        end = time.time()
        return {
            "err": "hh",
            "email": mail,
            "password": passwrd,
            "time_elapsed": end - start
        }
    except:
        return {"err": "Something unexpected happened. Please Try Again !"}
