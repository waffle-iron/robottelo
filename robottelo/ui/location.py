# -*- encoding: utf-8 -*-
"""Implements Locations UI"""
from robottelo.constants import FILTER
from robottelo.ui.base import Base
from robottelo.ui.locators import common_locators, locators, tab_locators
from robottelo.ui.navigator import Navigator


class Location(Base):
    """Implements CRUD functions for UI"""

    def navigate_to_entity(self):
        """Navigate to Locations entity page"""
        Navigator(self.browser).go_to_loc()

    def _search_locator(self):
        """Specify locator for Locations entity search procedure"""
        return locators['location.select_name']

    def _configure_location(self, users=None, capsules=None, subnets=None,
                            resources=None, medias=None, templates=None,
                            ptables=None, domains=None, envs=None,
                            hostgroups=None, organizations=None,
                            new_users=None, new_capsules=None,
                            new_subnets=None, new_resources=None,
                            new_medias=None, new_templates=None,
                            new_ptables=None, new_domains=None, new_envs=None,
                            new_hostgroups=None, new_organizations=None,
                            select=None):
        """Configures different entities of selected location."""

        loc = tab_locators

        if users or new_users:
            self.configure_entity(users, FILTER['loc_user'],
                                  tab_locator=loc['context.tab_users'],
                                  new_entity_list=new_users,
                                  entity_select=select)
        if capsules or new_capsules:
            self.configure_entity(capsules, FILTER['loc_capsules'],
                                  tab_locator=loc['context.tab_capsules'],
                                  new_entity_list=new_capsules,
                                  entity_select=select)
        if subnets or new_subnets:
            self.configure_entity(subnets, FILTER['loc_subnet'],
                                  tab_locator=loc['context.tab_subnets'],
                                  new_entity_list=new_subnets,
                                  entity_select=select)
        if resources or new_resources:
            self.configure_entity(resources, FILTER['loc_resource'],
                                  tab_locator=loc['context.tab_resources'],
                                  new_entity_list=new_resources,
                                  entity_select=select)
        if medias or new_medias:
            self.configure_entity(medias, FILTER['loc_media'],
                                  tab_locator=loc['context.tab_media'],
                                  new_entity_list=new_medias,
                                  entity_select=select)
        if templates or new_templates:
            self.configure_entity(templates, FILTER['loc_template'],
                                  tab_locator=loc['context.tab_template'],
                                  new_entity_list=new_templates,
                                  entity_select=select)
        if ptables or new_ptables:
            self.configure_entity(ptables, FILTER['loc_ptable'],
                                  tab_locator=loc['context.tab_ptable'],
                                  new_entity_list=new_ptables,
                                  entity_select=select)
        if domains or new_domains:
            self.configure_entity(domains, FILTER['loc_domain'],
                                  tab_locator=loc['context.tab_domains'],
                                  new_entity_list=new_domains,
                                  entity_select=select)
        if envs or new_envs:
            self.configure_entity(envs, FILTER['loc_envs'],
                                  tab_locator=loc['context.tab_env'],
                                  new_entity_list=new_envs,
                                  entity_select=select)
        if hostgroups or new_hostgroups:
            self.configure_entity(hostgroups, FILTER['loc_hostgroup'],
                                  tab_locator=loc['context.tab_hostgrps'],
                                  new_entity_list=new_hostgroups,
                                  entity_select=select)
        if organizations or new_organizations:
            self.configure_entity(hostgroups, FILTER['loc_org'],
                                  tab_locator=loc['context.tab_organizations'],
                                  new_entity_list=new_organizations,
                                  entity_select=select)

    def create(self, name, parent=None, users=None, capsules=None,
               subnets=None, resources=None, medias=None, templates=None,
               ptables=None, domains=None, envs=None, hostgroups=None,
               organizations=None, select=True):
        """Creates new Location from UI."""
        self.click(locators['location.new'])
        self.text_field_update(locators['location.name'], name)
        if parent:
            self.select(locators['location.parent'], parent)
        self.click(common_locators['submit'])
        self._configure_location(
            users=users, capsules=capsules,
            subnets=subnets, resources=resources,
            medias=medias, templates=templates,
            ptables=ptables, domains=domains, envs=envs,
            hostgroups=hostgroups,
            organizations=organizations,
            select=select,
        )
        self.click(common_locators['submit'])

    def update(self, loc_name, new_name=None, users=None,
               capsules=None, subnets=None, resources=None, medias=None,
               templates=None, ptables=None, domains=None, envs=None,
               hostgroups=None, organizations=None, new_organizations=None,
               new_users=None, new_capsules=None, new_subnets=None,
               new_resources=None, new_medias=None, new_templates=None,
               new_ptables=None, new_domains=None, new_envs=None,
               new_hostgroups=None, select=False):
        """Update Location in UI."""
        org_object = self.search(loc_name)
        self.click(org_object)
        if new_name:
            if self.wait_until_element(locators['location.name']):
                self.field_update('location.name', new_name)
        self._configure_location(users=users, capsules=capsules,
                                 subnets=subnets, resources=resources,
                                 medias=medias, templates=templates,
                                 ptables=ptables, domains=domains, envs=envs,
                                 hostgroups=hostgroups,
                                 organizations=organizations,
                                 new_organizations=new_organizations,
                                 new_users=new_users,
                                 new_capsules=new_capsules,
                                 new_subnets=new_subnets,
                                 new_resources=new_resources,
                                 new_medias=new_medias,
                                 new_templates=new_templates,
                                 new_ptables=new_ptables,
                                 new_domains=new_domains,
                                 new_envs=new_envs,
                                 new_hostgroups=new_hostgroups,
                                 select=select)
        self.click(common_locators['submit'])

    def delete(self, name, really=True):
        """Deletes a location."""
        self.delete_entity(
            name,
            really,
            locators['location.delete'],
            locators['location.dropdown'],
        )
