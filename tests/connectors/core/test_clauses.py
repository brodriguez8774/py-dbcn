"""
Initialization of "clause" logic of "Core" DB Connector class.

Note that the tests for the "Core" DB Connector class don't do anything in themselves.
They're meant to define a majority of overall database logic, which is then inherited/tweaked by the
various specific database test classes. This ensures that all databases types run similar/equal tests.
"""

# System Imports.

# Internal Imports.


class CoreClauseTestMixin:
    """
    Tests "Core" DB Connector class database logic.
    """
    @classmethod
    def set_up_class(cls):
        """
        Acts as the equivalent of the UnitTesting "setUpClass()" function.

        However, since this is not inheriting from a given TestCase,
        calling the literal function here would override instead.
        """
        cls.test_db_name_start = cls.test_db_name_start.format(cls.db_type)

    def test__clause__select(self):
        """Test logic for parsing a SELECT clause."""
        validation_class = self.connector.validate

        with self.subTest('SELECT clause as Empty'):
            # With passing none.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, None)
            self.assertEqual(['*'], clause_object.array)
            self.assertText('*', str(clause_object))

            # With empty single-quote string.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, '')
            self.assertEqual(['*'], clause_object.array)
            self.assertText('*', str(clause_object))

            # With empty double-quote string.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, "")
            self.assertEqual(['*'], clause_object.array)
            self.assertText('*', str(clause_object))

            # With emtpy triple double-quote string.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, """""")
            self.assertEqual(['*'], clause_object.array)
            self.assertText('*', str(clause_object))

        with self.subTest('Basic SELECT clause - As str'):
            # With no quotes.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, 'id')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            # With single quotes.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, "'id'")
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            # With double quotes.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, '"id"')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            # With backtick quotes.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, '`id`')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, 'id, code, name')
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""("id", "code", "name")""", str(clause_object))

        with self.subTest('Basic SELECT clause - As list'):
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, ['id'])
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            clause_object = self.connector.validate.clauses.SelectClauseBuilder(
                validation_class,
                ['id', 'code', 'name'],
            )
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""("id", "code", "name")""", str(clause_object))

        with self.subTest('Basic SELECT clause - As tuple'):
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, ('id',))
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            clause_object = self.connector.validate.clauses.SelectClauseBuilder(
                validation_class,
                ('id', 'code', 'name'),
            )
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""("id", "code", "name")""", str(clause_object))

        with self.subTest('Values with function calls'):
            # Uppercase.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, 'COUNT(*)')
            self.assertEqual(['COUNT(*)'], clause_object.array)
            self.assertText("""(COUNT(*))""", str(clause_object))

            # Lowercase.
            clause_object = self.connector.validate.clauses.SelectClauseBuilder(validation_class, 'count(*)')
            self.assertEqual(['COUNT(*)'], clause_object.array)
            self.assertText("""(COUNT(*))""", str(clause_object))

    def test__clause__where(self):
        """Test logic for parsing a WHERE clause."""
        validation_class = self.connector.validate

        with self.subTest('WHERE clause as Empty'):
            # With passing none.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, None)
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty single-quote string.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, '')
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty double-quote string.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, "")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With emtpy triple double-quote string.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, """""")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

        with self.subTest('Basic WHERE clause - As str'):
            # With no quotes.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, """id = 'test'""")
            self.assertEqual([[]], clause_object._clause_connectors)
            self.assertEqual([""""id" = 'test'"""], clause_object.array)
            self.assertText("""WHERE ("id" = 'test')""", str(clause_object))

            # With single quotes.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, """'id' = 'test'""")
            self.assertEqual([[]], clause_object._clause_connectors)
            self.assertEqual([""""id" = 'test'"""], clause_object.array)
            self.assertText("""WHERE ("id" = 'test')""", str(clause_object))

            # With double quotes.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, """"id" = 'test'""")
            self.assertEqual([[]], clause_object._clause_connectors)
            self.assertEqual([""""id" = 'test'"""], clause_object.array)
            self.assertText("""WHERE ("id" = 'test')""", str(clause_object))

            # With backtick quotes.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, """`id` = 'test'""")
            self.assertEqual([[]], clause_object._clause_connectors)
            self.assertEqual([""""id" = 'test'"""], clause_object.array)
            self.assertText("""WHERE ("id" = 'test')""", str(clause_object))

        with self.subTest('WHERE clause - As str, using ANDs only'):
            # Without paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """col_1 = 1 AND col_2 = 2 AND col_3 = 3 AND col_4 = 4""",
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # With paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """(col_1 = 1) AND (col_2 = 2) AND (col_3 = 3) AND (col_4 = 4)""",
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # With bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """[col_1 = 1] AND [col_2 = 2] AND [col_3 = 3] AND [col_4 = 4]""",
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # Testing various formats, no separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """id = 'test' AND `code` = 1234 AND "name" = 'Test User'""",
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """(id = 'test') AND (`code` = 1234) AND ("name" = 'Test User')""",
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """[id = 'test'] AND [`code` = 1234] AND ["name" = 'Test User']""",
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

        with self.subTest('Basic WHERE clause - As str, using ORs only'):
            # Without paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """col_1 = 1 OR col_2 = 2 OR col_3 = 3 OR col_4 = 4""",
            )
            self.assertEqual([[], 'OR', [], 'OR', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) OR ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # With paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """(col_1 = 1) OR (col_2 = 2) OR (col_3 = 3) OR (col_4 = 4)""",
            )
            self.assertEqual([[], 'OR', [], 'OR', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) OR ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # With bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """[col_1 = 1] OR [col_2 = 2] OR [col_3 = 3] OR [col_4 = 4]""",
            )
            self.assertEqual([[], 'OR', [], 'OR', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) OR ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # Testing various formats, no separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """id = 'test' OR `code` = 1234 OR "name" = 'Test User'""",
            )
            self.assertEqual([[], 'OR', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) OR ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """(id = 'test') OR (`code` = 1234) OR ("name" = 'Test User')""",
            )
            self.assertEqual([[], 'OR', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) OR ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                """[id = 'test'] OR [`code` = 1234] OR ["name" = 'Test User']""",
            )
            self.assertEqual([[], 'OR', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) OR ("name" = 'Test User')""",
                str(clause_object),
            )

        with self.subTest('Basic WHERE clause - As list'):
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, ["""id = 'test'"""])
            self.assertEqual([[]], clause_object._clause_connectors)
            self.assertEqual([""""id" = 'test'"""], clause_object.array)
            self.assertText("""WHERE ("id" = 'test')""", str(clause_object))

        with self.subTest('Where clause - As list, using ANDs only'):
            # Note: Default combination of array assumes AND format.

            # Without paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""col_1 = 1 AND col_2 = 2""", """col_3 = 3 AND col_4 = 4"""],
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # With paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""(col_1 = 1) AND (col_2 = 2)""", """(col_3 = 3) AND (col_4 = 4)"""],
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # With bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""[col_1 = 1] AND [col_2 = 2]""", """[col_3 = 3] AND [col_4 = 4]"""],
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # Testing various formats, no separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""id = 'test'""", """`code` = 1234""", """"name" = 'Test User'"""],
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""(id = 'test')""", """(`code` = 1234)""", """("name" = 'Test User')"""],
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""[id = 'test']""", """[`code` = 1234]""", """["name" = 'Test User']"""],
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

        with self.subTest('Where clause - As list, using ORs only'):
            # Note: Default combination of array assumes AND format.

            # Without paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""col_1 = 1 OR col_2 = 2""", """col_3 = 3 OR col_4 = 4"""],
            )
            self.assertEqual([[], 'OR', [], 'AND', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) AND ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # With paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""(col_1 = 1) OR (col_2 = 2)""", """(col_3 = 3) OR (col_4 = 4)"""],
            )
            self.assertEqual([[], 'OR', [], 'AND', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) AND ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # With bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""[col_1 = 1] OR [col_2 = 2]""", """[col_3 = 3] OR [col_4 = 4]"""],
            )
            self.assertEqual([[], 'OR', [], 'AND', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) AND ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # Testing various formats, no separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""id = 'test' OR `code` = 1234""", """"name" = 'Test User'"""],
            )
            self.assertEqual([[], 'OR', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""(id = 'test') OR (`code` = 1234)""", """("name" = 'Test User')"""],
            )
            self.assertEqual([[], 'OR', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ["""[id = 'test'] OR [`code` = 1234]""", """["name" = 'Test User']"""],
            )
            self.assertEqual([[], 'OR', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

        with self.subTest('Basic WHERE clause - As tuple'):
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(validation_class, ("""id = 'test'""",))
            self.assertEqual([[]], clause_object._clause_connectors)
            self.assertEqual([""""id" = 'test'"""], clause_object.array)
            self.assertText("""WHERE ("id" = 'test')""", str(clause_object))

        with self.subTest('Where clause - As tuple, using ANDs only'):
            # Note: Default combination of array assumes AND format.

            # Without paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""col_1 = 1 AND col_2 = 2""", """col_3 = 3 AND col_4 = 4"""),
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # With paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""(col_1 = 1) AND (col_2 = 2)""", """(col_3 = 3) AND (col_4 = 4)"""),
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # With bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""[col_1 = 1] AND [col_2 = 2]""", """[col_3 = 3] AND [col_4 = 4]"""),
            )
            self.assertEqual([[], 'AND', [], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) AND ("col_2" = 2) AND ("col_3" = 3) AND ("col_4" = 4)""",
                str(clause_object),
            )

            # Testing various formats, no separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""id = 'test'""", """`code` = 1234""", """"name" = 'Test User'"""),
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""(id = 'test')""", """(`code` = 1234)""", """("name" = 'Test User')"""),
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""[id = 'test']""", """[`code` = 1234]""", """["name" = 'Test User']"""),
            )
            self.assertEqual([[], 'AND', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') AND ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

        with self.subTest('Where clause - As list, using ORs only'):
            # Note: Default combination of array assumes AND format.

            # Without paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""col_1 = 1 OR col_2 = 2""", """col_3 = 3 OR col_4 = 4"""),
            )
            self.assertEqual([[], 'OR', [], 'AND', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) AND ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # With paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""(col_1 = 1) OR (col_2 = 2)""", """(col_3 = 3) OR (col_4 = 4)"""),
            )
            self.assertEqual([[], 'OR', [], 'AND', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) AND ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # With bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""[col_1 = 1] OR [col_2 = 2]""", """[col_3 = 3] OR [col_4 = 4]"""),
            )
            self.assertEqual([[], 'OR', [], 'AND', [], 'OR', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""col_1" = 1""", """"col_2" = 2""", """"col_3" = 3""", """"col_4" = 4"""],
                clause_object.array,
            )
            self.assertText(
                """WHERE ("col_1" = 1) OR ("col_2" = 2) AND ("col_3" = 3) OR ("col_4" = 4)""",
                str(clause_object),
            )

            # Testing various formats, no separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""id = 'test' OR `code` = 1234""", """"name" = 'Test User'"""),
            )
            self.assertEqual([[], 'OR', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with paren separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""(id = 'test') OR (`code` = 1234)""", """("name" = 'Test User')"""),
            )
            self.assertEqual([[], 'OR', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

            # Testing various formats, with bracket separators.
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""[id = 'test'] OR [`code` = 1234]""", """["name" = 'Test User']"""),
            )
            self.assertEqual([[], 'OR', [], 'AND', []], clause_object._clause_connectors)
            self.assertEqual(
                [""""id" = 'test'""", """"code" = 1234""", """"name" = 'Test User'"""],
                clause_object.array)
            self.assertText(
                """WHERE ("id" = 'test') OR ("code" = 1234) AND ("name" = 'Test User')""",
                str(clause_object),
            )

        with self.subTest('WHERE containing various quote types'):
            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""name = '2" nail'""", """description = '2 inch nail'"""""),
            )
            self.assertEqual([[], 'AND', []], clause_object._clause_connectors)
            self.assertEqual([""""name" = '2" nail'""", """"description" = '2 inch nail'"""], clause_object.array)
            self.assertText("""WHERE ("name" = '2" nail') AND ("description" = '2 inch nail')""", str(clause_object))

            clause_object = self.connector.validate.clauses.WhereClauseBuilder(
                validation_class,
                ("""name = '1\' ruler'""", """description = '1 foot ruler'"""""),
            )
            self.assertEqual([[], 'AND', []], clause_object._clause_connectors)
            # self.assertEqual([""""name" = '1\' ruler'""", """"description" = '1 foot ruler'"""], clause_object.array)
            self.assertText("""WHERE ("name" = '1\' ruler') AND ("description" = '1 foot ruler')""", str(clause_object))

    def test__clause__columns(self):
        """Test logic for parsing a COLUMNS clause."""
        validation_class = self.connector.validate

        with self.subTest('COLUMNS clause as Empty'):
            # With passing none.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, None)
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty single-quote string.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, '')
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty double-quote string.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, "")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With emtpy triple double-quote string.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, """""")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

        with self.subTest('Basic COLUMNS clause - As str'):
            # With no quotes.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, 'id')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            # With single quotes.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, "'id'")
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            # With double quotes.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, '"id"')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            # With backtick quotes.
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, '`id`')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, 'id, code, name')
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""("id", "code", "name")""", str(clause_object))

        with self.subTest('Basic COLUMNS clause - As list'):
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, ['id'])
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(
                validation_class,
                ['id', 'code', 'name'],
            )
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""("id", "code", "name")""", str(clause_object))

        with self.subTest('Basic COLUMNS clause - As tuple'):
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(validation_class, ('id',))
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""("id")""", str(clause_object))

            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(
                validation_class,
                ('id', 'code', 'name'),
            )
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""("id", "code", "name")""", str(clause_object))

        with self.subTest('Standard COLUMNS clause - As str'):
            clause_object = self.connector.validate.clauses.ColumnsClauseBuilder(
                validation_class,
                (
                    'id INT NOT NULL AUTO_INCREMENT, '
                    'title VARCHAR(100) NOT NULL, '
                    'description VARCHAR(255) NOT NULL'
                ),
            )
            self.assertEqual(
                [
                    '"id" INT NOT NULL AUTO_INCREMENT',
                    '"title" VARCHAR(100) NOT NULL',
                    '"description" VARCHAR(255) NOT NULL',
                ],
                clause_object.array,
            )
            self.assertText(
                """("id" INT NOT NULL AUTO_INCREMENT, "title" VARCHAR(100) NOT NULL, "description" VARCHAR(255) NOT NULL)""",
                str(clause_object),
            )

    def test__clause__values(self):
        """Test logic for paring a VALUES clause."""
        validation_class = self.connector.validate

        with self.subTest('VALUES clause as Empty'):
            # With passing none.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, None)
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty single-quote string.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, '')
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty double-quote string.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, "")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With emtpy triple double-quote string.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, """""")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

        with self.subTest('Basic VALUES clause - As str'):
            # With no quotes.
            # NOTE: To account for things like ints, we do not do space formatting unless they're already provided.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, """test""")
            self.assertEqual(["""test"""], clause_object.array)
            self.assertText("""VALUES (test)""", str(clause_object))

            # With single quotes.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, """'test'""")
            self.assertEqual(["""'test'"""], clause_object.array)
            self.assertText("""VALUES ('test')""", str(clause_object))

            # With double quotes.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, """"test\"""")
            self.assertEqual(["""'test'"""], clause_object.array)
            self.assertText("""VALUES ('test')""", str(clause_object))

            # With backtick quotes.
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, """`test`""")
            self.assertEqual(["""'test'"""], clause_object.array)
            self.assertText("""VALUES ('test')""", str(clause_object))

            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, """'test', 1234, 'Test User'""")
            self.assertEqual(["""'test'""", """1234""", """'Test User'"""], clause_object.array)
            self.assertText("""VALUES ('test', 1234, 'Test User')""", str(clause_object))

        with self.subTest('Basic VALUES clause - As list'):
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, ["""'test'"""])
            self.assertEqual(["""'test'"""], clause_object.array)
            self.assertText("""VALUES ('test')""", str(clause_object))

            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(
                validation_class,
                ["""'test'""", """1234""", """'Test User'"""],
            )
            self.assertEqual(["""'test'""", """1234""", """'Test User'"""], clause_object.array)
            self.assertText("""VALUES ('test', 1234, 'Test User')""", str(clause_object))

        with self.subTest('Basic VALUES clause - As tuple'):
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, ("""'test'""",))
            self.assertEqual(["""'test'"""], clause_object.array)
            self.assertText("""VALUES ('test')""", str(clause_object))

            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(
                validation_class,
                ("""'test'""", """1234""", """'Test User'"""),
            )
            self.assertEqual(["""'test'""", """1234""", """'Test User'"""], clause_object.array)
            self.assertText("""VALUES ('test', 1234, 'Test User')""", str(clause_object))

        with self.subTest('VALUES containing various quote types'):
            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, ("""'2" nail'""", """'2 inch nail'"""""))
            self.assertEqual(["""'2" nail'""", """'2 inch nail'"""], clause_object.array)
            self.assertText("""VALUES ('2" nail', '2 inch nail')""", str(clause_object))

            clause_object = self.connector.validate.clauses.ValuesClauseBuilder(validation_class, ("""'1\' ruler'""", """'1 foot ruler'"""""))
            self.assertEqual(["""'1\' ruler'""", """'1 foot ruler'"""], clause_object.array)
            self.assertText("""VALUES ('1\' ruler', '1 foot ruler')""", str(clause_object))

    def test__clause__order_by(self):
        """Test logic for parsing an ORDER BY clause."""
        validation_class = self.connector.validate

        with self.subTest('ORDER BY clause as Empty'):
            # With passing none.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, None)
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty single-quote string.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, '')
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With empty double-quote string.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, "")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

            # With emtpy triple double-quote string.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, """""")
            self.assertEqual([], clause_object.array)
            self.assertText('', str(clause_object))

        with self.subTest('Basic ORDER BY clause - As str'):
            # With no quotes.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, 'id')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""ORDER BY "id\"""", str(clause_object))

            # With single quotes.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, "'id'")
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""ORDER BY "id\"""", str(clause_object))

            # With double quotes.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, '"id"')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""ORDER BY "id\"""", str(clause_object))

            # With backtick quotes.
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, '`id`')
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""ORDER BY "id\"""", str(clause_object))

            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, 'id, code, name')
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""ORDER BY "id", "code", "name\"""", str(clause_object))

        with self.subTest('Basic ORDER BY clause - As list'):
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, ['id'])
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""ORDER BY "id\"""", str(clause_object))

            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(
                validation_class,
                ['id', 'code', 'name'],
            )
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""ORDER BY "id", "code", "name\"""", str(clause_object))

        with self.subTest('Basic ORDER BY clause - As tuple'):
            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(validation_class, ('id',))
            self.assertEqual(['"id"'], clause_object.array)
            self.assertText("""ORDER BY "id\"""", str(clause_object))

            clause_object = self.connector.validate.clauses.OrderByClauseBuilder(
                validation_class,
                ('id', 'code', 'name'),
            )
            self.assertEqual(['"id"', '"code"', '"name"'], clause_object.array)
            self.assertText("""ORDER BY "id", "code", "name\"""", str(clause_object))

    def test__clause__limit(self):
        """Test logic for paring a LIMIT clause."""
        validation_class = self.connector.validate
