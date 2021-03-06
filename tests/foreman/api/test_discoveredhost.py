# -*- encoding: utf-8 -*-
"""API Tests for foreman discovery feature

@Requirement: Discoveredhost

@CaseAutomation: Automated

@CaseLevel: Acceptance

@CaseComponent: API

@TestType: Functional

@CaseImportance: High

@Upstream: No
"""
from fauxfactory import gen_string, gen_ipaddr, gen_mac
from nailgun import entities
from robottelo.datafactory import valid_data_list
from robottelo.decorators import (
    run_only_on,
    skip_if_bug_open,
    stubbed,
    tier2,
    tier3,
)
from robottelo.test import APITestCase


def _create_discovered_host(name=None, ipaddress=None, macaddress=None):
    """Creates discovered host by uploading few fake facts.

    :param str name: Name of discovered host. If ``None`` then a random
        value will be generated.
    :param str ipaddress: A valid ip address.
        If ``None`` then then a random value will be generated.
    :param str macaddress: A valid mac address.
        If ``None`` then then a random value will be generated.
    :return: A ``dict`` of ``DiscoveredHost`` facts.
    """
    if name is None:
        name = gen_string('alpha')
    if ipaddress is None:
        ipaddress = gen_ipaddr()
    if macaddress is None:
        macaddress = gen_mac()
    return entities.DiscoveredHost().facts(json={
        u'facts': {
            u'name': name,
            u'discovery_bootip': ipaddress,
            u'discovery_bootif': macaddress,
            u'interfaces': 'eth0',
            u'ipaddress': ipaddress,
            u'macaddress': macaddress,
            u'macaddress_eth0': macaddress,
            u'ipaddress_eth0': ipaddress,
        }
    })


class DiscoveryTestCase(APITestCase):
    """Implements tests for foreman discovery feature"""

    @stubbed()
    @tier3
    def test_positive_list_all(self):
        """List all discovered hosts

        @id: ac3b49d6-87a2-4d36-8085-72113b14ffb5

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:

        1. GET /api/v2/discovered_hosts

        @Assert: List of all discovered hosts are retrieved

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_show(self):
        """Show a specific discovered hosts

        @id: f607838d-bbbb-40d6-b58e-e8eea6ef3d1d

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:

        1. GET /api/v2/discovered_hosts/:id

        @Assert: Selected host is retrieved

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_create(self):
        """Create a discovered hosts

        @id: b8f68ff0-6fda-46a0-aaea-ca2e714e3bec

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:

        1. POST /api/v2/discovered_hosts

        @Assert: Host should be created successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @run_only_on('sat')
    @skip_if_bug_open('bugzilla', 1349364)
    @tier2
    def test_positive_upload_facts(self):
        """Upload fake facts to create a discovered host

        @id: c1f40204-bbb0-46d0-9b60-e42f00ad1649

        @Steps:

        1. POST /api/v2/discovered_hosts/facts

        @Assert: Host should be created successfully

        @CaseLevel: Integration
        """
        for name in valid_data_list():
            with self.subTest(name):
                host = _create_discovered_host(name)
                host_name = 'mac{0}'.format(host['mac'].replace(':', ''))
                self.assertEqual(host['name'], host_name)

    @stubbed()
    @tier3
    def test_positive_provision_pxe_less_host(self):
        """Provision a pxe-less discovered hosts

        @id: 91bb254b-3c30-4608-b1ba-e18bcc22efb5

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:

        1. PUT /api/v2/discovered_hosts/:id

        @Assert: Host should be provisioned successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_provision_pxe_host(self):
        """Provision a pxe-based discovered hosts

        @id: e805b9c5-e8f6-4129-a0e6-ab54e5671ddb

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:
        1. PUT /api/v2/discovered_hosts/:id

        @Assert: Host should be provisioned successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_delete_pxe_less_host(self):
        """Delete a pxe-less discovered hosts

        @id: e8604ee4-04e9-4bb5-9487-18ab37ea271d

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:

        1. DELETE /api/v2/discovered_hosts/:id

        @Assert: Discovered Host should be deleted successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_delete_pxe_host(self):
        """Delete a pxe-based discovered hosts

        @id: 2ab2ad88-4470-4d4c-8e0b-5892ad8d675e

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:
        1. DELETE /api/v2/discovered_hosts/:id

        @Assert: Discovered Host should be deleted successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_auto_provision_pxe_less_host(self):
        """Auto provision a pxe-less host by executing discovery rules

        @id: 80a4be02-517a-4d41-bacc-a3f9dce47bdf

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:

        1. POST /api/v2/discovered_hosts/:id/auto_provision

        @Assert: Selected Host should be auto-provisioned successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_auto_provision_pxe_host(self):
        """Auto provision a pxe-based host by executing discovery rules

        @id: c93fd7c9-41ef-4eb5-8042-f72e87e67e10

        @Setup: Provisioning should be configured and a host should be
        discovered

        @Steps:
        1. POST /api/v2/discovered_hosts/:id/auto_provision

        @Assert: Selected Host should be auto-provisioned successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_auto_provision_all(self):
        """Auto provision all host by executing discovery rules

        @id: 954d3688-62d9-47f7-9106-a4fff8825ffa

        @Setup: Provisioning should be configured and more than one host should
        be discovered

        @Steps:

        1. POST /api/v2/discovered_hosts/auto_provision_all

        @Assert: All discovered hosts should be auto-provisioned successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_refresh_facts_pxe_less_host(self):
        """Refreshing the facts of pxe-less discovered host by adding a new NIC.

        @id: c6ef642e-5eb1-4297-bad1-48f88a1660c6

        @Setup:

        1. Provisioning should be configured and more than one host should
        be discovered via discovery ISO

        2. Add a NIC on discovered host

        @Steps:

        1. PUT /api/v2/discovered_hosts/:id/refresh_facts

        @Assert: Added Fact should be displayed on refreshing the facts

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_refresh_facts_pxe_host(self):
        """Refresh the facts of pxe based discovered hosts by adding a new NIC

        @id: 413fb608-cd5c-441d-af86-fd2d40346d96

        @Setup:
        1. Provisioning should be configured and more than one host should
        be discovered

        2. Add a NIC on discovered host

        @Steps:
        1. PUT /api/v2/discovered_hosts/:id/refresh_facts

        @Assert: Added Fact should be displayed on refreshing the facts

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_reboot_pxe_host(self):
        """Rebooting a pxe based discovered host

        @id: 69c807f8-5646-4aa6-8b3c-5ecab69560fc

        @Setup: Provisioning should be configured and more than one host should
        be discovered via PXE boot.

        @Steps:

        1. PUT /api/v2/discovered_hosts/:id/reboot

        @Assert: Selected host should be rebooted successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_reboot_pxe_less_host(self):
        """Rebooting a pxe-less discovered host

        @id: 2e7bdf3c-fb5d-44da-981d-d4ba9ffaba60

        @Setup: Provisioning should be configured and more than one host should
        be discovered using discovery ISO.

        @Steps:
        1. PUT /api/v2/discovered_hosts/:id/reboot

        @Assert: Selected host should be rebooted successfully

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_provision_host_with_rule(self):
        """Create a new discovery rule and applies on host to provision

        Set query as (e.g IP=IP_of_discovered_host)

        @id: a5531225-0b5f-4999-925f-4f40f77e20f8

        @Setup: Host should already be discovered

        @Assert: Host should reboot and provision

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_provision_multihost_with_rule(self):
        """Create a new discovery rule with (host_limit = 0)
        that applies to multi hosts.
        Set query as cpu_count = 1 OR mem > 500

        @id: 19ce9ac0-e915-41b3-8c2d-2b17e5fbe42a

        @Setup: Multiple hosts should already be discovered in same subnet

        @Assert: All Hosts of same subnet should reboot and provision

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_provision_with_rule_priority(self):
        """Create multiple discovery rules with different priority and check
        rule with highest priority executed first

        @id: b91c4979-f8ce-4f6e-9474-9ccd4c3bc793

        @Setup: Multiple hosts should already be discovered

        @Assert: Host with lower count have higher priority
        and that rule should be executed first

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_multi_provision_with_rule_limit(self):
        """Create a discovery rule (CPU_COUNT = 2) with host limit 1 and
        provision more than one host with same rule

        @id: 553c8ebf-d1c1-4ac2-9948-d3664a5b450b

        @Setup: Host with two CPUs should already be discovered

        @Assert: Rule should only be applied to one discovered host and for
        other rule should already be skipped.

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_provision_with_updated_discovery_rule(self):
        """Update an existing rule and provision a host with it.

        @id: 3fb20e0f-02e9-4158-9744-f583308c4e89

        @Setup: Host should already be discovered

        @Assert: User should be able to update the rule and it should be
        applied on discovered host

        @caseautomation: notautomated

        @CaseLevel: System
        """

    @stubbed()
    @tier3
    def test_positive_provision_with_updated_hostname_in_rule(self):
        """Update the discovered hostname in existing rule and provision a host
        with it

        @id: aaa1d6ac-0f52-4b1f-9bfe-853169985621

        @Setup: Host should already be discovered

        @Assert: The host name should be updated and host should be provisioned

        @caseautomation: notautomated

        @CaseLevel: System
        """
