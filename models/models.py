# -*- coding: utf-8 -*-

from odoo import models, fields, api, http
from datetime import date

MAX_DAYS = 2147483647


class Test(models.Model):
    _name = 'test.test'
    # _description = 'test.test'

    name = fields.Char('Name')
    purpose = fields.Text('Purpose')
    tester = fields.Many2one('res.partner', 'Tester', default=lambda self: self.env.user.partner_id)
    test_session = fields.One2many('test.session', 'test', 'Session')
    min_days_to_start = fields.Integer(compute='_compute_min_days_to_start', string="Min days to start")

    def _min_days_to_start(self):
        self.ensure_one()
        days_list = [(test_session.start_date - date.today()).days for test_session in self.test_session]
        if days_list:
            return min(days_list)
        else:
            return MAX_DAYS

    @api.depends('test_session')
    def _compute_min_days_to_start(self):
        for test in self:
            test.min_days_to_start = test._min_days_to_start()


class TestSession(models.Model):
    _name = 'test.session'

    display_name = fields.Char('Display Name', compute="_compute_display_name")
    test = fields.Many2one('test.test', 'Test', ondelete='restrict')
    start_date = fields.Date('Start Date', default=fields.Date.today)
    end_date = fields.Date('End Date')
    duration = fields.Float(compute='_compute_duration', string="Duration")

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for test_entry in self:
            test_entry.duration = test_entry._get_duration(test_entry.start_date, test_entry.end_date)

    @api.depends('test', 'start_date')
    def _compute_display_name(self):
        for test_session in self:
            test_session.display_name = '{} {}'.format(test_session.test.name, test_session.start_date)

    def _get_duration(self, start_date, end_date):
        if not start_date or not end_date:
            return 0
        dt = end_date - start_date
        return dt.days
        # return dt.days * 24 + dt.seconds / 3600  # Number of hours

    def write(self, vals):
        session = super(TestSession, self).write(vals)
        self.test.tester._compute_min_days_to_start()
        return session

    @api.model
    def create(self, vals):
        session = super(TestSession, self).create(vals)
        session.test.tester._compute_min_days_to_start()
        return session

    def unlink(self):
        tester = self.test.tester
        session = super(TestSession, self).unlink()
        tester._compute_min_days_to_start()
        return session


class TestPartner(models.Model):
    _inherit = 'res.partner'

    is_tester = fields.Boolean(compute='_compute_is_tester', string="isTester")
    tests_ids = fields.One2many('test.test', 'tester', 'Tests')
    min_days_to_start = fields.Integer(compute='_compute_min_days_to_start', string="Min days to start", store=True)

    @api.depends('tests_ids')
    def _compute_is_tester(self):
        for partner in self:
            partner.is_tester = True if partner.tests_ids else False

    @api.depends('tests_ids')
    def _compute_min_days_to_start(self):
        for partner in self:
            days_list = [test.min_days_to_start for test in partner.tests_ids]
            partner.min_days_to_start = min(days_list) if days_list else MAX_DAYS
