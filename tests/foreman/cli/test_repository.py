# -*- encoding: utf-8 -*-
"""Test class for Repository CLI

@Requirement: Repository

@CaseAutomation: Automated

@CaseLevel: Acceptance

@CaseComponent: CLI

@TestType: Functional

@CaseImportance: High

@Upstream: No
"""

from fauxfactory import gen_string
from robottelo import ssh
from robottelo.cli.base import CLIReturnCodeError
from robottelo.cli.task import Task
from robottelo.cli.factory import (
    make_gpg_key,
    make_org,
    make_product_wait,
    make_repository,
    CLIFactoryError
)
from robottelo.cli.repository import Repository
from robottelo.constants import (
    DOCKER_REGISTRY_HUB,
    FAKE_0_YUM_REPO,
    FAKE_1_PUPPET_REPO,
    FAKE_1_YUM_REPO,
    FAKE_2_PUPPET_REPO,
    FAKE_2_YUM_REPO,
    FAKE_3_PUPPET_REPO,
    FAKE_3_YUM_REPO,
    FAKE_4_PUPPET_REPO,
    FAKE_4_YUM_REPO,
    FAKE_5_PUPPET_REPO,
    FAKE_5_YUM_REPO,
    FAKE_7_PUPPET_REPO,
    RPM_TO_UPLOAD,
)
from robottelo.decorators import (
    run_only_on,
    skip_if_bug_open,
    stubbed,
    tier1,
    tier2,
)
from robottelo.datafactory import (
    invalid_http_credentials,
    invalid_values_list,
    valid_data_list,
    valid_http_credentials,
)
from robottelo.helpers import get_data_file
from robottelo.test import CLITestCase


class RepositoryTestCase(CLITestCase):
    """Repository CLI tests."""

    org = None
    product = None

    # pylint: disable=unexpected-keyword-arg
    def setUp(self):
        """Tests for Repository via Hammer CLI"""

        super(RepositoryTestCase, self).setUp()

        if RepositoryTestCase.org is None:
            RepositoryTestCase.org = make_org(cached=True)
        if RepositoryTestCase.product is None:
            RepositoryTestCase.product = make_product_wait(
                {u'organization-id': RepositoryTestCase.org['id']},
                )

    def _make_repository(self, options=None):
        """Makes a new repository and asserts its success"""
        if options is None:
            options = {}

        if options.get('product-id') is None:
            options[u'product-id'] = self.product['id']

        return make_repository(options)

    @tier1
    def test_verify_bugzilla_1189289(self):
        """Check if repository docker-upstream-name is shown
        in repository info

        @id: f197a14c-2cf3-4564-9b18-5fd37d469ea4

        @Assert: repository info command returns upstream-repository-name
        value
        """
        repository = self._make_repository({
            u'content-type': u'docker',
            u'name': gen_string('alpha'),
            u'docker-upstream-name': u'fedora/rabbitmq',
        })
        self.assertIn(u'upstream-repository-name', repository)
        self.assertEqual(
            repository['upstream-repository-name'], u'fedora/rabbitmq')

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_name(self):
        """Check if repository can be created with random names

        @id: 604dea2c-d512-4a27-bfc1-24c9655b6ea9

        @Assert: Repository is created and has random name
        """
        for name in valid_data_list():
            with self.subTest(name):
                new_repo = self._make_repository({u'name': name})
                self.assertEqual(new_repo['name'], name)

    @tier1
    def test_positive_create_with_name_label(self):
        """Check if repository can be created with random names and
        labels

        @id: 79d2a6d0-5032-46cd-880c-46cf392521fa

        @Assert: Repository is created and has random name and labels
        """
        for name in valid_data_list():
            with self.subTest(name):
                # Generate a random, 'safe' label
                label = gen_string('alpha', 20)
                new_repo = self._make_repository({
                    u'label': label,
                    u'name': name,
                })
                self.assertEqual(new_repo['name'], name)
                self.assertNotEqual(new_repo['name'], new_repo['label'])

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_yum_repo(self):
        """Create YUM repository

        @id: 4c08824f-ba95-486c-94c2-9abf0a3441ea

        @Assert: YUM repository is created
        """
        for url in (FAKE_0_YUM_REPO, FAKE_1_YUM_REPO, FAKE_2_YUM_REPO,
                    FAKE_3_YUM_REPO, FAKE_4_YUM_REPO):
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'yum',
                    u'url': url,
                })
                self.assertEqual(new_repo['url'], url)
                self.assertEqual(new_repo['content-type'], u'yum')

    @tier1
    def test_positive_create_with_puppet_repo(self):
        """Create Puppet repository

        @id: 75c309ba-fbc9-419d-8427-7a61b063ec13

        @Assert: Puppet repository is created
        """
        for url in (FAKE_1_PUPPET_REPO, FAKE_2_PUPPET_REPO, FAKE_3_PUPPET_REPO,
                    FAKE_4_PUPPET_REPO, FAKE_5_PUPPET_REPO):
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'puppet',
                    u'url': url,
                })
                self.assertEqual(new_repo['url'], url)
                self.assertEqual(new_repo['content-type'], u'puppet')

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_auth_yum_repo(self):
        """Create YUM repository with basic HTTP authentication

        @id: da8309fd-3076-427b-a96f-8d883d6e944f

        @Assert: YUM repository is created
        """
        url = FAKE_5_YUM_REPO
        for creds in valid_http_credentials(url_encoded=True):
            url_encoded = url.format(creds['login'], creds['pass'])
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'yum',
                    u'url': url_encoded
                })
                self.assertEqual(new_repo['url'], url_encoded)
                self.assertEqual(new_repo['content-type'], u'yum')

    @tier1
    def test_positive_create_with_auth_puppet_repo(self):
        """Create Puppet repository with basic HTTP authentication

        @id: b13f8ae2-60ab-47e6-a096-d3f368e5cab3

        @Assert: Puppet repository is created
        """
        url = FAKE_7_PUPPET_REPO
        for creds in valid_http_credentials(url_encoded=True):
            url_encoded = url.format(creds['login'], creds['pass'])
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'puppet',
                    u'url': url_encoded
                })
                self.assertEqual(new_repo['url'], url_encoded)
                self.assertEqual(new_repo['content-type'], u'puppet')

    @run_only_on('sat')
    @tier1
    def test_positive_create_with_gpg_key_by_id(self):
        """Check if repository can be created with gpg key ID

        @id: 6d22f0ea-2d27-4827-9b7a-3e1550a47285

        @Assert: Repository is created and has gpg key
        """
        # Make a new gpg key
        gpg_key = make_gpg_key({'organization-id': self.org['id']})
        for name in valid_data_list():
            with self.subTest(name):
                new_repo = self._make_repository({
                    u'gpg-key-id': gpg_key['id'],
                    u'name': name,
                })
                self.assertEqual(new_repo['gpg-key']['id'], gpg_key['id'])
                self.assertEqual(new_repo['gpg-key']['name'], gpg_key['name'])

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1103944)
    @tier1
    def test_positive_create_with_gpg_key_by_name(self):
        """Check if repository can be created with gpg key name

        @id: 95cde404-3449-410d-9a08-d7f8619a2ad5

        @Assert: Repository is created and has gpg key

        @BZ: 1103944
        """
        gpg_key = make_gpg_key({'organization-id': self.org['id']})
        for name in valid_data_list():
            with self.subTest(name):
                new_repo = self._make_repository({
                    u'gpg-key': gpg_key['name'],
                    u'name': name,
                    u'organization-id': self.org['id'],
                })
                self.assertEqual(new_repo['gpg-key']['id'], gpg_key['id'])
                self.assertEqual(new_repo['gpg-key']['name'], gpg_key['name'])

    @run_only_on('sat')
    @tier1
    def test_positive_create_publish_via_http(self):
        """Create repository published via http

        @id: faf6058c-9dd3-444c-ace2-c41791669e9e

        @Assert: Repository is created and is published via http
        """
        for use_http in u'true', u'yes', u'1':
            with self.subTest(use_http):
                repo = self._make_repository({'publish-via-http': use_http})
                self.assertEqual(repo['publish-via-http'], u'yes')

    @run_only_on('sat')
    @tier1
    def test_positive_create_publish_via_https(self):
        """Create repository not published via http

        @id: 4395a5df-207c-4b34-a42d-7b3273bd68ec

        @Assert: Repository is created and is not published via http
        """
        for use_http in u'false', u'no', u'0':
            with self.subTest(use_http):
                repo = self._make_repository({'publish-via-http': use_http})
                self.assertEqual(repo['publish-via-http'], u'no')

    @run_only_on('sat')
    @tier1
    def test_positive_create_yum_repo_with_checksum_type(self):
        """Create a YUM repository with a checksum type

        @id: 934f4a09-2a64-485d-ae6c-8ef73aa8fb2b

        @Assert: A YUM repository is created and contains the correct checksum
        type
        """
        for checksum_type in u'sha1', u'sha256':
            with self.subTest(checksum_type):
                content_type = u'yum'
                repository = self._make_repository({
                    u'checksum-type': checksum_type,
                    u'content-type': content_type,
                })
                self.assertEqual(repository['content-type'], content_type)
                self.assertEqual(repository['checksum-type'], checksum_type)

    @run_only_on('sat')
    @tier1
    def test_positive_create_docker_repo_with_upstream_name(self):
        """Create a Docker repository with upstream name.

        @id: 776f92eb-8b40-4efd-8315-4fbbabcb2d4e

        @Assert: Docker repository is created and contains correct values.
        """
        content_type = u'docker'
        new_repo = self._make_repository({
            u'content-type': content_type,
            u'docker-upstream-name': u'busybox',
            u'name': u'busybox',
            u'url': DOCKER_REGISTRY_HUB,
        })
        # Assert that urls and content types matches data passed
        self.assertEqual(new_repo['url'], DOCKER_REGISTRY_HUB)
        self.assertEqual(new_repo['content-type'], content_type)
        self.assertEqual(new_repo['name'], u'busybox')

    @run_only_on('sat')
    @tier1
    def test_positive_create_docker_repo_with_name(self):
        """Create a Docker repository with a random name.

        @id: b6a01434-8672-4196-b61a-dcb86c49f43b

        @Assert: Docker repository is created and contains correct values.
        """
        for name in valid_data_list():
            with self.subTest(name):
                content_type = u'docker'
                new_repo = self._make_repository({
                    u'content-type': content_type,
                    u'docker-upstream-name': u'busybox',
                    u'name': name,
                    u'url': DOCKER_REGISTRY_HUB,
                })
                # Assert that urls, content types and name matches data passed
                self.assertEqual(new_repo['url'], DOCKER_REGISTRY_HUB)
                self.assertEqual(new_repo['content-type'], content_type)
                self.assertEqual(new_repo['name'], name)

    @tier1
    def test_negative_create_with_name(self):
        """Repository name cannot be 300-characters long

        @id: af0652d3-012d-4846-82ac-047918f74722

        @Assert: Repository cannot be created
        """
        for name in invalid_values_list():
            with self.subTest(name):
                with self.assertRaises(CLIFactoryError):
                    self._make_repository({u'name': name})

    @tier1
    def test_negative_create_with_auth_url_with_special_characters(self):
        """Verify that repository URL cannot contain unquoted special characters

        @id: 2bd5ee17-0fe5-43cb-9cdc-dc2178c5374c

        @Assert: Repository cannot be created
        """
        # get a list of valid credentials without quoting them
        for cred in [creds for creds in valid_http_credentials()
                     if creds['quote'] is True]:
            with self.subTest(cred):
                url = FAKE_5_YUM_REPO.format(cred['login'], cred['pass'])
                with self.assertRaises(CLIFactoryError):
                    self._make_repository({u'url': url})

    @tier1
    def test_negative_create_with_auth_url_too_long(self):
        """Verify that repository URL length is limited

        @id: de356c66-4237-4421-89e3-f4f8bbe6f526

        @Assert: Repository cannot be created
        """
        for cred in invalid_http_credentials():
            with self.subTest(cred):
                url = FAKE_5_YUM_REPO.format(cred['login'], cred['pass'])
                with self.assertRaises(CLIFactoryError):
                    self._make_repository({u'url': url})

    @run_only_on('sat')
    @tier2
    def test_positive_synchronize_yum_repo(self):
        """Check if repository can be created and synced

        @id: e3a62529-edbd-4062-9246-bef5f33bdcf0

        @Assert: Repository is created and synced

        @CaseLevel: Integration
        """
        for url in FAKE_1_YUM_REPO, FAKE_3_YUM_REPO, FAKE_4_YUM_REPO:
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'yum',
                    u'url': url,
                })
                # Assertion that repo is not yet synced
                self.assertEqual(new_repo['sync']['status'], 'Not Synced')
                # Synchronize it
                Repository.synchronize({'id': new_repo['id']})
                # Verify it has finished
                new_repo = Repository.info({'id': new_repo['id']})
                self.assertEqual(new_repo['sync']['status'], 'Success')

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1328092)
    @tier2
    def test_positive_synchronize_auth_yum_repo(self):
        """Check if secured repository can be created and synced

        @id: b0db676b-e0f0-428c-adf3-1d7c0c3599f0

        @Assert: Repository is created and synced

        @CaseLevel: Integration
        """
        url = FAKE_5_YUM_REPO
        for creds in [cred for cred in valid_http_credentials(url_encoded=True)
                      if cred['http_valid']]:
            url_encoded = url.format(
                creds['login'], creds['pass']
            )
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'yum',
                    u'url': url_encoded,
                })
                # Assertion that repo is not yet synced
                self.assertEqual(new_repo['sync']['status'], 'Not Synced')
                # Synchronize it
                Repository.synchronize({'id': new_repo['id']})
                # Verify it has finished
                new_repo = Repository.info({'id': new_repo['id']})
                self.assertEqual(new_repo['sync']['status'], 'Success')

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1328092)
    @tier2
    def test_negative_synchronize_auth_yum_repo(self):
        """Check if secured repo fails to synchronize with invalid credentials

        @id: 809905ae-fb76-465d-9468-1f99c4274aeb

        @Assert: Repository is created but synchronization fails

        @CaseLevel: Integration
        """
        url = FAKE_5_YUM_REPO
        for creds in [cred for cred in valid_http_credentials(url_encoded=True)
                      if not cred['http_valid']]:
            url_encoded = url.format(
                creds['login'], creds['pass']
            )
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'yum',
                    u'url': url_encoded,
                })
                # Try to synchronize it
                repo_sync = Repository.synchronize(
                    {'id': new_repo['id'], u'async': True}
                )
                Task.progress({u'id': repo_sync[0]['id']})
                self.assertEqual(
                    Task.progress({u'id': repo_sync[0]['id']})[0],
                    u'Yum Metadata: Unauthorized'
                )

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1328092)
    @tier2
    def test_positive_synchronize_auth_puppet_repo(self):
        """Check if secured puppet repository can be created and synced

        @id: 1d2604fc-8a18-4cbe-bf4c-5c7d9fbdb82c

        @Assert: Repository is created and synced

        @CaseLevel: Integration
        """
        url = FAKE_7_PUPPET_REPO
        for creds in [cred for cred in valid_http_credentials(url_encoded=True)
                      if cred['http_valid']]:
            url_encoded = url.format(creds['login'], creds['pass'])
            with self.subTest(url):
                new_repo = self._make_repository({
                    u'content-type': u'yum',
                    u'url': url_encoded,
                })
                # Assertion that repo is not yet synced
                self.assertEqual(new_repo['sync']['status'], 'Not Synced')
                # Synchronize it
                Repository.synchronize({'id': new_repo['id']})
                # Verify it has finished
                new_repo = Repository.info({'id': new_repo['id']})
                self.assertEqual(new_repo['sync']['status'], 'Success')

    @run_only_on('sat')
    @tier2
    def test_positive_synchronize_docker_repo(self):
        """Check if Docker repository can be created and synced

        @id: cb9ae788-743c-4785-98b2-6ae0c161bc9a

        @Assert: Docker repository is created and synced

        @CaseLevel: Integration
        """
        new_repo = self._make_repository({
            u'content-type': u'docker',
            u'docker-upstream-name': u'busybox',
            u'url': DOCKER_REGISTRY_HUB,
        })
        # Assertion that repo is not yet synced
        self.assertEqual(new_repo['sync']['status'], 'Not Synced')
        # Synchronize it
        Repository.synchronize({'id': new_repo['id']})
        # Verify it has finished
        new_repo = Repository.info({'id': new_repo['id']})
        self.assertEqual(new_repo['sync']['status'], 'Success')

    @run_only_on('sat')
    @tier1
    def test_positive_update_url(self):
        """Update the original url for a repository

        @id: 1a2cf29b-5c30-4d4c-b6d1-2f227b0a0a57

        @Assert: Repository url is updated
        """
        new_repo = self._make_repository()
        # generate repo URLs with all valid credentials
        auth_repos = [
            repo.format(creds['login'], creds['pass'])
            for creds in valid_http_credentials(url_encoded=True)
            for repo in (FAKE_5_YUM_REPO, FAKE_7_PUPPET_REPO)
        ]

        for url in [FAKE_4_YUM_REPO, FAKE_1_PUPPET_REPO, FAKE_2_PUPPET_REPO,
                    FAKE_3_PUPPET_REPO, FAKE_2_YUM_REPO] + auth_repos:
            with self.subTest(url):
                # Update the url
                Repository.update({
                    u'id': new_repo['id'],
                    u'url': url,
                })
                # Fetch it again
                result = Repository.info({'id': new_repo['id']})
                self.assertEqual(result['url'], url)

    @run_only_on('sat')
    @tier1
    def test_negative_update_auth_url_with_special_characters(self):
        """Verify that repository URL credentials cannot be updated to contain
        the forbidden characters

        @id: 566553b2-d077-4fd8-8ed5-00ba75355386

        @Assert: Repository url not updated
        """
        new_repo = self._make_repository()
        # get auth repos with credentials containing unquoted special chars
        auth_repos = [
            repo.format(cred['login'], cred['pass'])
            for cred in valid_http_credentials() if cred['quote']
            for repo in (FAKE_5_YUM_REPO, FAKE_7_PUPPET_REPO)
        ]

        for url in auth_repos:
            with self.subTest(url):
                with self.assertRaises(CLIReturnCodeError):
                    Repository.update({
                        u'id': new_repo['id'],
                        u'url': url,
                    })
                # Fetch it again
                result = Repository.info({'id': new_repo['id']})
                self.assertEqual(result['url'], new_repo['url'])

    @run_only_on('sat')
    @tier1
    def test_negative_update_auth_url_too_long(self):
        """Update the original url for a repository to value which is too long

        @id: a703de60-8631-4e31-a9d9-e51804f27f03

        @Assert: Repository url not updated
        """
        new_repo = self._make_repository()
        # generate repo URLs with all invalid credentials
        auth_repos = [
            repo.format(cred['login'], cred['pass'])
            for cred in invalid_http_credentials()
            for repo in (FAKE_5_YUM_REPO, FAKE_7_PUPPET_REPO)
        ]

        for url in auth_repos:
            with self.subTest(url):
                with self.assertRaises(CLIReturnCodeError):
                    Repository.update({
                        u'id': new_repo['id'],
                        u'url': url,
                    })
                # Fetch it again
                result = Repository.info({'id': new_repo['id']})
                self.assertEqual(result['url'], new_repo['url'])

    @run_only_on('sat')
    @stubbed()
    def test_positive_update_gpg_key(self):
        """Update the original gpg key

        @id: 367ff375-4f52-4a8c-b974-8c1c54e3fdd3

        @Assert: Repository gpg key is updated

        @caseautomation: notautomated
        """

    @run_only_on('sat')
    @stubbed()
    def test_positive_update_published_method(self):
        """Update the original publishing method

        @id: e7bd2667-4851-4a64-9c70-1b5eafbc3f71

        @Assert: Repository publishing method is updated

        @caseautomation: notautomated
        """

    @run_only_on('sat')
    @tier1
    def test_positive_update_checksum_type(self):
        """Create a YUM repository and update the checksum type

        @id: 42f14257-d860-443d-b337-36fd355014bc

        @Assert: A YUM repository is updated and contains the correct checksum
        type
        """
        content_type = u'yum'
        repository = self._make_repository({
            u'content-type': content_type
        })
        self.assertEqual(repository['content-type'], content_type)
        for checksum_type in u'sha1', u'sha256':
            with self.subTest(checksum_type):
                # Update the checksum
                Repository.update({
                    u'checksum-type': checksum_type,
                    u'id': repository['id'],
                })
                # Fetch it again
                result = Repository.info({'id': repository['id']})
                self.assertEqual(result['checksum-type'], checksum_type)

    @run_only_on('sat')
    @tier1
    def test_positive_delete_by_id(self):
        """Check if repository can be created and deleted

        @id: bcf096db-0033-4138-90a3-cb7355d5dfaf

        @Assert: Repository is created and then deleted
        """
        for name in valid_data_list():
            with self.subTest(name):
                new_repo = self._make_repository({u'name': name})
                Repository.delete({u'id': new_repo['id']})
                with self.assertRaises(CLIReturnCodeError):
                    Repository.info({u'id': new_repo['id']})

    @skip_if_bug_open('bugzilla', 1343006)
    @tier1
    def test_positive_upload_content(self):
        """Create repository and upload content

        @id: eb0ec599-2bf1-483a-8215-66652f948d67

        @Assert: upload content is successful
        """
        new_repo = self._make_repository({'name': gen_string('alpha', 15)})
        ssh.upload_file(local_file=get_data_file(RPM_TO_UPLOAD),
                        remote_file="/tmp/{0}".format(RPM_TO_UPLOAD))
        result = Repository.upload_content({
            'name': new_repo['name'],
            'organization': new_repo['organization'],
            'path': "/tmp/{0}".format(RPM_TO_UPLOAD),
            'product-id': new_repo['product']['id'],
        })
        self.assertIn(
            "Successfully uploaded file '{0}'".format(RPM_TO_UPLOAD),
            result[0]['message'],
        )
