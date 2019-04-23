from django.test import TestCase
from test_plus.test import TestCase
from django.conf import settings
from .models import Board
from .forms import BoardForm

#1. settigs test
class SettingsTest(TestCase):
    def test_01_settings(self):
        self.assertEqual(settings.USE_I18N, True)
        self.assertEqual(settings.LANGUAGE_CODE, 'ko-kr')
        self.assertEqual(settings.TIME_ZONE, 'Asia/Seoul')
        self.assertEqual(settings.USE_TZ, False)

#2. Model test
class BoardModelTest(TestCase):
    def test_01_model(self):
        # board = Board.objects.create(title='test title', content='test content')
        board = Board.objects.create(title='test title', content='test content', user_id=1)
        self.assertEqual(str(board), f'Board{board.pk}', msg='출력 값이 일치하지 않음')
        
#3. View Test
class BoardViewTest(TestCase):
    # 고정적으로 로그인 되도록 공통적인 given 상황을 구성하기에 유용
    def setUp(self):
        user = self.make_user(username='test', password='asdfghjk!')
    

    
    # create test 에서의 포인트는 form을 제대로 주느냐이다. 가장 기본은 get_check_200 (성공)
    def test_01_get_create(self):
        #GIVEN
        # user = self.make_user(username='test', password='asdfghjk!')
        #WHEN
        with self.login(username='test', password='asdfghjk!'):
        # login 상태를 유지시켜주는 것
            response = self.get_check_200('boards:create')
            # self.assertContains(response, '<form')
            # 받은 응답이 첫번째 인자임
            # THEN 더 정확한 코드
            self.assertIsInstance(response.context['form'], BoardForm)
    
    def test_02_get_create_login_required(self):
        self.assertLoginRequired('boards:create')
        
        
    def test_03_post_create(self):
        # given 사용자와 작성한 글 데이터
        # user = self.make_user(username='test', password='asdfghjk!')
        data = {'title':'test title', 'content':'test content'}
        # when 로그인해서 post 요청으로 해당 url로 요청 보낸 경우
        with self.login(username='test', password='asdfghjk!'):
            # then 글이 작성되고, 페이지가 detail로 redirect 된다
            self.post('boards:create', data=data)
        
    
    def test_04_board_create_without_content(self):
        #given 
        data = {'title': 'test title'}
        # when
        with self.login(username='test', password='asdfghjk!'):
            response = self.post('boards:create', data=data)
            self.assertContains(response, '폼에 필수항목입니다')
            # form.is_valid()를 통과하지 못해 튕겨져 나옴
         # assertContains response 해당하는 글자가 있는지 확인하는 메소드
         

            

        
        
        