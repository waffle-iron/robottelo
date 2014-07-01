"""Tests for module ``robottelo.factories``."""
# (Too many public methods) pylint: disable=R0904
from fauxfactory import FauxFactory
from robottelo import factories, orm
from sys import version_info
from unittest import TestCase


class EmptyEntity(orm.Entity):
    """A sample entity which has no fields."""


class NonEmptyEntity(orm.Entity):
    """A sample entity which has fields."""
    name = orm.StringField(required=True)
    cost = orm.IntegerField()


class GetPopulateStringFieldTestCase(TestCase):
    """"Tests for method ``_populate_string_field``."""
    # (protected-access) pylint:disable=W0212
    def test_unicode(self):
        """Check whether a unicode string is returned."""
        string = factories._populate_string_field()
        if version_info[0] == 2:
            self.assertIsInstance(string, unicode)
        else:
            self.assertIsInstance(string, str)

    def test_len(self):
        """Check whether a string at least 1 char long is returned."""
        self.assertTrue(len(factories._populate_string_field()) > 0)


class IsRequiredTestCase(TestCase):
    """Test for function ``_is_required``."""
    # (protected-access) pylint:disable=W0212
    def test__is_required_v1(self):
        """Do not set the ``required`` attribute at all.

        Assert that ``_is_required`` returns ``False``.

        """
        self.assertFalse(factories._is_required(orm.Field()))

    def test__is_required_v2(self):
        """Set the ``required`` attribute to ``False``.

        Assert that ``_is_required`` returns ``False``.

        """
        self.assertFalse(factories._is_required(orm.Field(required=False)))

    def test__is_required_v3(self):
        """Set the ``required`` attribute to ``True``.

        Assert that ``_is_required`` returns ``True``.

        """
        self.assertTrue(factories._is_required(orm.Field(required=True)))


class FactoryTestCase(TestCase):
    """Tests for class ``Factory``."""
    def test__customize_field_names_v1(self):
        """Call ``_customize_field_names`` without altering ``Meta``.

        Create several factories using ``NonEmptyEntity`` and with
        ``interface`` set to default, ``'API'`` and ``'CLI'``. Ensure
        ``_customize_field_names`` produces correct output in each case.

        """
        # (protected-access) pylint:disable=W0212
        factory = factories.Factory(NonEmptyEntity)
        fields = factory._customize_field_names(NonEmptyEntity.get_fields())
        self.assertIn('name', fields)
        self.assertIn('cost', fields)

        factory = factories.Factory(NonEmptyEntity, 'API')
        fields = factory._customize_field_names(NonEmptyEntity.get_fields())
        self.assertIn('name', fields)
        self.assertIn('cost', fields)

        factory = factories.Factory(NonEmptyEntity, 'CLI')
        fields = factory._customize_field_names(NonEmptyEntity.get_fields())
        self.assertIn('name', fields)
        self.assertIn('cost', fields)

    def test__customize_field_names_v2(self):
        """Set attributes on ``Meta`` and call ``_customize_field_names``.

        Set ``NonEmptyEntity.Meta.api_names`` and
        ``NonEmptyEntity.Meta.cli_names``. Create several factories using
        ``NonEmptyEntity`` and with ``interface`` set to default, ``'API'`` and
        ``'CLI'``. Ensure ``_customize_field_names`` produces correct output in
        each case.

        """
        # (protected-access) pylint:disable=W0212
        NonEmptyEntity.Meta.api_names = {'name': 'customized'}
        NonEmptyEntity.Meta.cli_names = {'cost': 'field_names'}

        factory = factories.Factory(NonEmptyEntity)
        fields = factory._customize_field_names(NonEmptyEntity.get_fields())
        self.assertIn('name', fields)
        self.assertIn('cost', fields)

        factory = factories.Factory(NonEmptyEntity, 'API')
        fields = factory._customize_field_names(NonEmptyEntity.get_fields())
        self.assertIn('customized', fields)
        self.assertIn('cost', fields)

        factory = factories.Factory(NonEmptyEntity, 'CLI')
        fields = factory._customize_field_names(NonEmptyEntity.get_fields())
        self.assertIn('name', fields)
        self.assertIn('field_names', fields)

    def test__customize_field_names_v3(self):
        """Set extra ``Meta`` attributes and call ``_customize_field_names``.

        Set ``EmptyEntity.Meta.api_names`` and ``EmptyEntity.Meta.cli_names``.
        Call ``_customize_field_names``, and ensure that the method does not
        complain about the missing underlying fields.

        """
        EmptyEntity.Meta.api_names = {'these_fields': 'do_not_exist'}
        EmptyEntity.Meta.cli_names = {'on': 'EmptyEntity'}

        factory = factories.Factory(EmptyEntity)
        fields = factory._customize_field_names(EmptyEntity.get_fields())
        self.assertEqual(fields, {})

        factory = factories.Factory(EmptyEntity, 'API')
        fields = factory._customize_field_names(EmptyEntity.get_fields())
        self.assertEqual(fields, {})

        factory = factories.Factory(EmptyEntity, 'CLI')
        fields = factory._customize_field_names(EmptyEntity.get_fields())
        self.assertEqual(fields, {})

    def test_attributes_v1(self):
        """Create a factory with ``EmptyEntity``, then call ``attributes``.

        Assert an empty dict is returned.

        """
        self.assertEqual({}, factories.Factory(EmptyEntity).attributes())

    def test_attributes_v2(self):
        """Create a factory with ``NonEmptyEntity``, then call ``attributes``.

        Assert the dict returned contains the correct keys, and that those keys
        correspond to the correct datatypes.

        """
        attrs = factories.Factory(NonEmptyEntity).attributes()
        self.assertEqual(len(attrs.keys()), 1)
        self.assertIn('name', attrs)
        self.assertEqual(
            type(factories._populate_string_field()),  # pylint:disable=W0212
            type(attrs['name'])
        )

    def test_attributes_v3(self):
        """Explicitly provide several values to the ``attributes`` method.

        Rather than letting ``Factory`` generate default values for all fields,
        pass several field values to the ``attributes`` method. Assert the
        values passed in are used in the dict of attributes returned.

        """
        # NonEmptyEntity.name is a required attribute
        name = FauxFactory.generate_string(
            'utf8',
            FauxFactory.generate_integer(1, 1000)
        )
        attrs = factories.Factory(NonEmptyEntity).attributes(name=name)
        self.assertEqual(attrs['name'], name)

        # NonEmptyEntity.name is a non-required attribute
        cost = FauxFactory.generate_integer(1, 1000)
        attrs = factories.Factory(NonEmptyEntity).attributes(
            name=name,
            cost=cost
        )
        self.assertEqual(attrs['name'], name)
        self.assertEqual(attrs['cost'], cost)

    def test_attributes_v4(self):
        """Provide non-existent fields to the ``attributes`` method.

        Assert that, if non-existent fields are provided to ``attributes``, a
        ``ValueException`` is raised.

        """
        with self.assertRaises(ValueError):
            factories.Factory(EmptyEntity).attributes(no_such_field='bad juju')
