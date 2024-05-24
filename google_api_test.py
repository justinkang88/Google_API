import unittest

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import HtmlTestRunner




class google_api_test(unittest.TestCase):
        
    #구글 API 요청을 위해 인증을 수행하는 함수, 가장 첫 순서로 호출
    def test_TC00_Pre_condition_make_credential(self): 
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        #구글 콘솔에서 다운 받은 인증파일을 credential.json으로 저장하여 참조
        flow = InstalledAppFlow.from_client_secrets_file('./credential.json', SCOPES)
        global creds
        creds = flow.run_local_server(port=8080)


    def test_TC01_update_location(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        
        calendar['location'] = 'test-location'
        updated_calendar = service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        # update 요청이 정상적으로 적용 되었는지 assertEqual를 활용하여 확인
        self.assertEqual(updated_calendar['location'], 'test-location')
        #ResourceWarning을 막기위해 테스트케이스마다 Service 종료
        service.close()

    

    def test_TC02_update_invalid_location(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['location'] = 'longtext'*10000    
        #예외처리 동작을 확인하기 위해 HttpError로 예외처리 메시지 확보 후 테스트 결과 판독에 활용    
        with self.assertRaises(HttpError) as context: 
            service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        ##에러 응답코드와 응답 메시지를 활용하여 결과 판독
        self.assertIn('HttpError 400', str(context.exception))
        self.assertIn('Invalid Value', str(context.exception))
        service.close()



    
    def test_TC03_update_timeZone(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['timeZone'] = 'Asia/Tokyo'
        updated_calendar = service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertEqual(updated_calendar['timeZone'], 'Asia/Tokyo')
        service.close()



    def test_TC04_update_invalid_timeZone(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['timeZone'] = 'invalid Text'        
        with self.assertRaises(HttpError) as context: 
            service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertIn('HttpError 400', str(context.exception))
        self.assertIn('Invalid Value', str(context.exception))
        service.close()



    def test_TC05_update_invalid_timeZone(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['timeZone'] = 'long Text'*1000        
        with self.assertRaises(HttpError) as context: 
            service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertIn('HttpError 400', str(context.exception))
        self.assertIn('Invalid Value', str(context.exception))
        service.close()


    
    def test_TC06_update_description(self):
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['description'] = 'New description222'
        updated_calendar = service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertEqual(updated_calendar['description'], 'New description222')
        service.close()



    def test_TC07_update_invalid_description(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['description'] = 'long Text'*1000        
        with self.assertRaises(HttpError) as context: 
            service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertIn('HttpError 400', str(context.exception))
        self.assertIn('Invalid Value', str(context.exception))
        service.close()



    def test_TC08_test_update_summary(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['summary'] = 'New summary222'
        updated_calendar = service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertEqual(updated_calendar['summary'], 'New summary222')
        service.close()


    
    def test_TC09_update_invalid_summary(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['summary'] = ''        
        with self.assertRaises(HttpError) as context: 
            service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertIn('HttpError 400', str(context.exception))
        self.assertIn('Missing summary', str(context.exception))
        service.close()



    def test_TC10_update_invalid_summary(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['summary'] = 'long Text'*1000        
        with self.assertRaises(HttpError) as context: 
            service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertIn('HttpError 400', str(context.exception))
        self.assertIn('A provided value exceeds the allowed size limit', str(context.exception))
        service.close()



    def test_TC11_update_invalid_calendarid(self) :
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId='primary').execute()
        calendar['id'] = 'invalidid'        
        with self.assertRaises(HttpError) as context: 
            service.calendars().update(calendarId=calendar['id'], body=calendar).execute()
        self.assertIn('HttpError 404', str(context.exception))
        self.assertIn('Not Found', str(context.exception))
        service.close()



    def tearDown(self):
        print("Test Complete :", self._testMethodName)



if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test-reports'))
    

