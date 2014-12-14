from collections import defaultdict
import unittest
import mock

from s3s import is_local_termination


class S3STestCase(unittest.TestCase):
    """Tests for config.py"""

    def setUp(self):
        self.json_template = u'{"EC2InstanceId":"%(instance_id)s","LifecycleTransition":"%(transition)s"}'
        self.message = mock.Mock()
        self.payload = self.json_template % {'instance_id': 'local', 'transition': 'autoscaling:EC2_INSTANCE_TERMINATING'}
        self.payload_not_json = u'this is not json'
        self.payload_not_lifecycle_hook = u'{}'
        self.payload_not_local_instance = self.json_template % {'instance_id': 'not-local', 'transition': 'autoscaling:EC2_INSTANCE_TERMINATING'}
        self.payload_not_termination = self.json_template % {'instance_id': 'local', 'transition': ''}

    def test_is_local_termination(self):
        with mock.patch('s3s.get_instance_id') as get_instance_id:
            get_instance_id.return_value = 'local'
            attrs = {'get_body.return_value': self.payload}
            self.message.configure_mock(**attrs)
            self.assertTrue(is_local_termination(self.message))

    def test_is_local_termination_not_json(self):
        attrs = {'get_body.return_value': self.payload_not_json}
        self.message.configure_mock(**attrs)
        self.assertFalse(is_local_termination(self.message))

    def test_is_local_termination_not_lifecycle_hook(self):
        with mock.patch('s3s.get_instance_id') as get_instance_id:
            get_instance_id.return_value = 'local'
            attrs = {'get_body.return_value': self.payload_not_lifecycle_hook}
            self.message.configure_mock(**attrs)
            self.assertFalse(is_local_termination(self.message))

    def test_is_local_termination_not_local_instance(self):
        with mock.patch('s3s.get_instance_id') as get_instance_id:
            get_instance_id.return_value = 'local'
            attrs = {'get_body.return_value': self.payload_not_local_instance}
            self.message.configure_mock(**attrs)
            self.assertFalse(is_local_termination(self.message))

    def test_is_local_termination_not_termination(self):
        with mock.patch('s3s.get_instance_id') as get_instance_id:
            get_instance_id.return_value = 'local'
            attrs = {'get_body.return_value': self.payload_not_termination}
            self.message.configure_mock(**attrs)
            self.assertFalse(is_local_termination(self.message))
