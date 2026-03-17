"""Initial database schema

Revision ID: 001
Revises: 
Create Date: 2026-03-17

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('username', sa.String(100), nullable=False, unique=True, index=True),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255)),
        sa.Column('avatar_url', sa.String(512)),
        sa.Column('role', sa.String(50), default='user'),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # projects
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('task_type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('priority', sa.Integer, default=0),
        sa.Column('goal_raw', sa.Text, nullable=False),
        sa.Column('goal_parsed', postgresql.JSONB, default={}),
        sa.Column('started_at', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.Column('estimated_duration', sa.Integer),
        sa.Column('actual_duration', sa.Integer),
        sa.Column('total_tasks', sa.Integer, default=0),
        sa.Column('completed_tasks', sa.Integer, default=0),
        sa.Column('total_messages', sa.Integer, default=0),
        sa.Column('total_decisions', sa.Integer, default=0),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('idx_projects_user_id', 'projects', ['user_id'])
    op.create_index('idx_projects_status', 'projects', ['status'])

    # agents
    op.create_table(
        'agents',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(100), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.String(1000)),
        sa.Column('agent_type', sa.String(50), nullable=False),
        sa.Column('capabilities', postgresql.JSONB, default=[]),
        sa.Column('tools', postgresql.JSONB, default=[]),
        sa.Column('llm_provider', sa.String(50), default='openai'),
        sa.Column('llm_model', sa.String(100)),
        sa.Column('llm_config', postgresql.JSONB, default={}),
        sa.Column('authority_level', sa.Integer, default=1),
        sa.Column('can_approve', sa.Boolean, default=False),
        sa.Column('can_delegate', sa.Boolean, default=False),
        sa.Column('status', sa.String(50), default='idle'),
        sa.Column('current_task_id', postgresql.UUID(as_uuid=True)),
        sa.Column('tasks_assigned', sa.Integer, default=0),
        sa.Column('tasks_completed', sa.Integer, default=0),
        sa.Column('messages_sent', sa.Integer, default=0),
        sa.Column('decisions_made', sa.Integer, default=0),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('idx_agents_project_id', 'agents', ['project_id'])

    # agent_relationships
    op.create_table(
        'agent_relationships',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('parent_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='CASCADE')),
        sa.Column('child_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='CASCADE')),
        sa.Column('relationship_type', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # tasks
    op.create_table(
        'tasks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('task_type', sa.String(100), nullable=False),
        sa.Column('owner_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('reviewer_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('approver_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('status', sa.String(50), default='pending'),
        sa.Column('priority', sa.Integer, default=0),
        sa.Column('depends_on', postgresql.JSONB, default=[]),
        sa.Column('estimated_duration', sa.Integer),
        sa.Column('actual_duration', sa.Integer),
        sa.Column('started_at', sa.DateTime(timezone=True)),
        sa.Column('completed_at', sa.DateTime(timezone=True)),
        sa.Column('input_data', postgresql.JSONB, default={}),
        sa.Column('output_data', postgresql.JSONB, default={}),
        sa.Column('execution_logs', postgresql.JSONB, default=[]),
        sa.Column('error_message', sa.Text),
        sa.Column('retry_count', sa.Integer, default=0),
        sa.Column('max_retries', sa.Integer, default=3),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('idx_tasks_project_id', 'tasks', ['project_id'])
    op.create_index('idx_tasks_status', 'tasks', ['status'])

    # task_dependencies
    op.create_table(
        'task_dependencies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('predecessor_task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('successor_task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False),
        sa.Column('dependency_type', sa.String(50), default='finish_to_start'),
    )

    # messages
    op.create_table(
        'messages',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='SET NULL')),
        sa.Column('sender_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('receiver_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('message_type', sa.String(50), nullable=False),
        sa.Column('subject', sa.String(500)),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('thread_id', postgresql.UUID(as_uuid=True)),
        sa.Column('parent_message_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('messages.id', ondelete='SET NULL')),
        sa.Column('attachments', postgresql.JSONB, default=[]),
        sa.Column('mentioned_agents', postgresql.JSONB, default=[]),
        sa.Column('is_read', sa.Boolean, default=False),
        sa.Column('is_important', sa.Boolean, default=False),
        sa.Column('requires_response', sa.Boolean, default=False),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('idx_messages_project_id', 'messages', ['project_id'])

    # decisions
    op.create_table(
        'decisions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='SET NULL')),
        sa.Column('decision_type', sa.String(100), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('made_by_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('approved_by_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('options_considered', postgresql.JSONB, default=[]),
        sa.Column('chosen_option', postgresql.JSONB, nullable=False),
        sa.Column('rationale', sa.Text, nullable=False),
        sa.Column('impact_scope', sa.String(50)),
        sa.Column('affected_tasks', postgresql.JSONB, default=[]),
        sa.Column('affected_agents', postgresql.JSONB, default=[]),
        sa.Column('status', sa.String(50), default='proposed'),
        sa.Column('proposed_at', sa.DateTime(timezone=True)),
        sa.Column('approved_at', sa.DateTime(timezone=True)),
        sa.Column('implemented_at', sa.DateTime(timezone=True)),
        sa.Column('outcome', sa.Text),
        sa.Column('was_successful', sa.Boolean),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('idx_decisions_project_id', 'decisions', ['project_id'])

    # outputs
    op.create_table(
        'outputs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('task_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tasks.id', ondelete='SET NULL')),
        sa.Column('output_type', sa.String(100), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('author_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('reviewed_by_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('approved_by_agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('content', sa.Text),
        sa.Column('file_path', sa.String(1000)),
        sa.Column('file_format', sa.String(50)),
        sa.Column('version', sa.String(50), default='1.0.0'),
        sa.Column('parent_output_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('outputs.id', ondelete='SET NULL')),
        sa.Column('is_latest', sa.Boolean, default=True),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('quality_score', sa.Numeric(3, 2)),
        sa.Column('review_comments', sa.Text),
        sa.Column('published_at', sa.DateTime(timezone=True)),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('idx_outputs_project_id', 'outputs', ['project_id'])

    # workflows
    op.create_table(
        'workflows',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text),
        sa.Column('graph_definition', postgresql.JSONB, nullable=False),
        sa.Column('status', sa.String(50), default='draft'),
        sa.Column('current_node', sa.String(100)),
        sa.Column('execution_state', postgresql.JSONB, default={}),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )

    # audit_logs
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE')),
        sa.Column('agent_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('agents.id', ondelete='SET NULL')),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('entity_type', sa.String(100), nullable=False),
        sa.Column('entity_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('old_values', postgresql.JSONB),
        sa.Column('new_values', postgresql.JSONB),
        sa.Column('metadata', postgresql.JSONB, default={}),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index('idx_audit_logs_entity', 'audit_logs', ['entity_type', 'entity_id'])


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_table('workflows')
    op.drop_table('outputs')
    op.drop_table('decisions')
    op.drop_table('messages')
    op.drop_table('task_dependencies')
    op.drop_table('tasks')
    op.drop_table('agent_relationships')
    op.drop_table('agents')
    op.drop_table('projects')
    op.drop_table('users')
