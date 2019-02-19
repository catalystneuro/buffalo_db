from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta
import json

from alyx import base
from alyx.base import BaseTests
from subjects.models import Subject, Project
from misc.models import Lab
from actions.models import Session, WaterType, WaterAdministration


class APIActionsTests(BaseTests):
    def setUp(self):
        base.DISABLE_MAIL = True
        self.superuser = get_user_model().objects.create_superuser('test', 'test', 'test')
        self.superuser2 = get_user_model().objects.create_superuser('test2', 'test2', 'test2')
        self.client.login(username='test', password='test')
        self.subject = Subject.objects.all().first()
        self.lab01 = Lab.objects.create(name='superlab')
        self.lab02 = Lab.objects.create(name='awesomelab')
        self.projectX = Project.objects.create(name='projectX')
        # Set an implant weight.
        self.subject.implant_weight = 4.56
        self.subject.save()
        self.test_protocol = 'test_passoire'

    def tearDown(self):
        base.DISABLE_MAIL = False

    def test_create_weighing(self):
        url = reverse('weighing-create')
        data = {'subject': self.subject, 'weight': 12.3}
        response = self.client.post(url, data)
        self.ar(response, 201)
        d = response.data
        self.assertTrue(d['date_time'])
        self.assertEqual(d['subject'], self.subject.nickname)
        self.assertEqual(d['weight'], 12.3)

    def test_create_water_administration(self):
        url = reverse('water-administration-create')
        ses_uuid = Session.objects.last().id
        water_type = WaterType.objects.last().name
        data = {'subject': self.subject, 'water_administered': 1.23,
                'session': ses_uuid, 'water_type': water_type}
        response = self.client.post(url, data)
        self.ar(response, 201)
        d = response.data
        self.assertTrue(d['date_time'])
        self.assertEqual(d['subject'], self.subject.nickname)
        self.assertEqual(d['water_administered'], 1.23)
        self.assertEqual(d['water_type'], water_type)
        self.assertEqual(d['session'], ses_uuid)

    def test_list_water_administration_1(self):
        url = reverse('water-administration-create')
        response = self.client.get(url)
        self.ar(response)
        d = response.data[0]
        self.assertTrue(set(('date_time', 'url', 'subject', 'user',
                             'water_administered', 'water_type')) <= set(d))

    def test_list_water_administration_filter(self):
        url = reverse('water-administration-create')
        data = {'subject': self.subject, 'water_administered': 1.23}
        response = self.client.post(url, data)

        url = reverse('water-administration-create') + '?nickname=' + self.subject.nickname
        response = self.client.get(url)
        self.ar(response)
        d = response.data[0]
        self.assertTrue(set(('date_time', 'url', 'subject', 'user',
                             'water_administered', 'water_type', 'adlib')) <= set(d))

    def test_list_weighing_1(self):
        url = reverse('weighing-create')
        response = self.client.get(url)
        self.ar(response)
        d = response.data[0]
        self.assertTrue(set(('date_time', 'url', 'subject', 'user', 'weight')) <= set(d))

    def test_list_weighing_filter(self):
        url = reverse('weighing-create')
        data = {'subject': self.subject, 'weight': 12.3}
        response = self.client.post(url, data)

        url = reverse('weighing-create') + '?nickname=' + self.subject.nickname
        response = self.client.get(url)
        self.ar(response)
        d = response.data[0]
        self.assertTrue(set(('date_time', 'url', 'subject', 'user', 'weight')) <= set(d))

    def test_water_requirement(self):
        # Create water administered and weighing.
        self.client.post(reverse('water-administration-create'),
                         {'subject': self.subject, 'water_administered': 1.23})
        self.client.post(reverse('weighing-create'),
                         {'subject': self.subject, 'weight': 12.3})

        url = reverse('water-requirement', kwargs={'nickname': self.subject.nickname})

        date = now().date()
        start_date = date - timedelta(days=2)
        end_date = date + timedelta(days=2)
        response = self.client.get(
            url + '?start_date=%s&end_date=%s' % (
                start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        self.ar(response)
        d = response.data
        self.assertEqual(d['subject'], self.subject.nickname)
        self.assertEqual(d['implant_weight'], 4.56)
        self.assertTrue(
            set(('date', 'weight', 'expected_weight', 'expected_water',
                 'given_water_reward', 'given_water_supplement',)) <= set(d['records'][0]))
        dates = sorted(_['date'] for _ in d['records'])
        assert len(dates) == 5
        assert dates[0] == start_date
        assert dates[-1] == end_date
        assert dates[2] == date

    def test_sessions(self):
        a_dict4json = {'String': 'this is not a JSON'}
        ses_dict = {'subject': self.subject,
                    'users': self.superuser,
                    'project': self.projectX.name,
                    'narrative': 'auto-generated-session, test',
                    'start_time': '2018-07-09T12:34:56',
                    'end_time': '2018-07-09T12:34:57',
                    'type': 'Base',
                    'number': '1',
                    'parent_session': '',
                    'lab': self.lab01,
                    'n_trials': 100,
                    'n_correct_trials': 75,
                    'task_protocol': self.test_protocol,
                    'json': json.dumps(a_dict4json)}
        # Test the session creation
        r = self.client.post(reverse('session-list'), ses_dict)
        self.ar(r, 201)
        s1_details = r.data
        # makes sure the task_protocol is returned
        self.assertEqual(self.test_protocol, s1_details['task_protocol'])
        # the json is in the session details
        r = self.client.get(reverse('session-list') + '/' + s1_details['url'][-36:])
        self.assertEqual(r.data['json'], a_dict4json)
        # but not in the session list
        r = self.client.get(reverse('session-list') + '?id=' + s1_details['url'][-36:])
        s1 = r.data[0]
        self.assertFalse('json' in s1)
        # create another session for further testing
        ses_dict['start_time'] = '2018-07-11T12:34:56'
        ses_dict['end_time'] = '2018-07-11T12:34:57'
        ses_dict['users'] = [self.superuser, self.superuser2]
        ses_dict['lab'] = self.lab02
        ses_dict['n_correct_trials'] = 37
        r = self.client.post(reverse('session-list'), ses_dict)
        s2 = r.data
        s2.pop('json')
        # Test the date range filter
        r = self.client.get(reverse('session-list') + '?date_range=2018-07-09,2018-07-09')
        self.assertEqual(r.data[0], s1)
        # Test the user filter, this should return 2 sessions
        r = self.client.get(reverse('session-list') + '?users=test')
        self.assertTrue(len(r.data) == 2)
        # This should return only one session
        r = self.client.get(reverse('session-list') + '?users=test2')
        self.assertEqual(r.data[0], s2)
        # This should return only one session
        r = self.client.get(reverse('session-list') + '?lab=awesomelab')
        self.assertEqual(r.data[0], s2)
        # Test performance: gte, lte and ensures null performances not included
        r = self.client.get(reverse('session-list') + '?performance_gte=50')
        self.assertEqual(r.data[0]['url'], s1['url'])
        self.assertTrue(len(r.data) == 1)
        r = self.client.get(reverse('session-list') + '?performance_lte=50')
        self.assertEqual(r.data[0]['url'], s2['url'])
        self.assertTrue(len(r.data) == 1)
        # test the Session serializer wateradmin related field
        ses = Session.objects.get(subject=self.subject, users=self.superuser,
                                  project=self.projectX, start_time__date='2018-07-09')
        WaterAdministration.objects.create(subject=self.subject, session=ses, water_administered=1)
        r = self.client.get(reverse('session-list') + '?date_range=2018-07-09,2018-07-09')
        self.ar(r)
        self.assertEqual(r.data[0]['wateradmin_session_related'][0]['water_administered'], 1)

    def test_list_retrieve_water_restrictions(self):
        url = reverse('water-restriction-list')
        response = self.client.get(url)
        self.ar(response)
        d = response.data[0]
        self.assertTrue(set(d.keys()) >= set(['reference_weight', 'water_type', 'subject',
                                              'start_time', 'end_time']))
        url = url = reverse('water-restriction-list') + '?subject=' + d['subject']
        response = self.client.get(url)
        self.ar(response)
        d2 = response.data[0]
        self.assertEqual(d, d2)
