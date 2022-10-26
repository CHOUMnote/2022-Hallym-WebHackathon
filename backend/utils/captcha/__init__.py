"""
Copyright 2013 TY<tianyu0915@gmail.com>
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import time
import random

from PIL import Image, ImageDraw, ImageFont


class Captcha(object):
    def __init__(self, request):
        """
        초기화 및 속성 설정
        """
        self.django_request = request
        self.session_key = "_django_captcha_key"
        self.captcha_expires_time = "_django_captcha_expires_time"

        # 인증 코드 이미지 크기
        self.img_width = 90
        self.img_height = 30

    def _get_font_size(self, code):
        """
        이미지 높이의 80%를 글꼴 크기로 사용
        """
        s1 = int(self.img_height * 0.8)
        s2 = int(self.img_width / len(code))
        return int(min((s1, s2)) + max((s1, s2)) * 0.05)

    def _set_answer(self, answer):
        """
        답변 및 만료 시간 설정
        """
        self.django_request.session[self.session_key] = str(answer)
        self.django_request.session[self.captcha_expires_time] = time.time() + (5 * 60) # email 인증을 위한 시간 고려

    def _make_code(self):
        """
        난수 또는 난수 문자열 생성
        """
        string = random.sample("abcdefghkmnpqrstuvwxyzABCDEFGHGKMNOPQRSTUVWXYZ23456789", 4)
        self._set_answer("".join(string))
        return string

    def get(self):
        """
        인증 코드 이미지 생성, 반환 값은 이미지의 바이트
        """
        background = (random.randrange(200, 255), random.randrange(200, 255), random.randrange(200, 255))
        code_color = (random.randrange(0, 50), random.randrange(0, 50), random.randrange(0, 50), 255)

        font_path = os.path.join(os.path.normpath(os.path.dirname(__file__)), "timesbi.ttf")

        image = Image.new("RGB", (self.img_width, self.img_height), background)
        code = self._make_code()
        font_size = self._get_font_size(code)
        draw = ImageDraw.Draw(image)

        # x는 첫 번째 문자의 x 좌표임
        x = random.randrange(int(font_size * 0.3), int(font_size * 0.5))

        for i in code:
            # 문자 y 좌표
            y = random.randrange(1, 7)
            # 임의의 문자 크기
            font = ImageFont.truetype(font_path.replace("\\", "/"), font_size + random.randrange(-3, 7))
            draw.text((x, y), i, font=font, fill=code_color)
            # 문자 사이의 거리를 무작위화; 문자를 붙이면 인식률이 떨어질 수 있으니 주의
            x += font_size * random.randrange(6, 8) / 10

        self.django_request.session[self.session_key] = "".join(code)
        return image

    def check(self, code):
        """
        检查用户输入的验证码是否正确
        """
        _code = self.django_request.session.get(self.session_key) or ""
        if not _code:
            return False
        expires_time = self.django_request.session.get(self.captcha_expires_time) or 0
        # 인증 후 이전 인증코드를 지우지 않으면 중복 인증이 발생할 수 있으니 유의
        del self.django_request.session[self.session_key]
        del self.django_request.session[self.captcha_expires_time]
        if _code.lower() == str(code).lower() and time.time() < expires_time:
            return True
        else:
            return False
