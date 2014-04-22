# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""create dictionary tables

Revision ID: 001
Revises: None
Create Date: 2014-03-18 07:36:33.498311

"""

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'namespaces',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('scope', sa.String(length=255), nullable=False),
        sa.Column('owner', sa.String(length=2000), nullable=False),
        sa.PrimaryKeyConstraint('name')
    )
    op.create_table(
        'capability_types',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('namespace', sa.String(length=255),
                  sa.ForeignKey('namespaces.name', onupdate="CASCADE",
                                ondelete="CASCADE"),
                  nullable=False),
        sa.Column('description', sa.String(length=2000), nullable=True),
        sa.Column('parent_name', sa.String(length=255), nullable=True),
        sa.Column('parent_namespace', sa.String(length=255), nullable=True),
        sa.Column('properties_text', sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint('name', 'namespace'),
        sa.ForeignKeyConstraint(['parent_name', 'parent_namespace'],
                                ['capability_types.name',
                                 'capability_types.namespace'],
                                onupdate="CASCADE", ondelete="CASCADE")
    )


def downgrade():
    op.drop_table('capability_types')
    op.drop_table('namespaces')
