from odoo import models


class IDPhotoSyncMixin(models.AbstractModel):
    _name = 'idphoto.sync.mixin'
    _description = 'ID Photo Sync Mixin for User, Employee, Partner'

    def _get_linked_user_employee_partner(self):
        """Return (users, employees, partners) recordsets linked to *self*."""
        self.ensure_one()
        users = self.env['res.users']
        partners = self.env['res.partner']
        employees = self.env['hr.employee']

        if self._name == 'res.users':
            users |= self
            if self.partner_id:
                partners |= self.partner_id
            if self.employee_id:
                employees |= self.employee_id
        elif self._name == 'hr.employee':
            employees |= self
            if self.user_id:
                users |= self.user_id
            if self.address_id:
                partners |= self.address_id
        elif self._name == 'res.partner':
            partners |= self
            if self.user_ids:
                users |= self.user_ids
            if hasattr(self, 'employee_ids') and self.employee_ids:
                employees |= self.employee_ids

        return users, employees, partners

    def _sync_image_to_linked(self, target_models):
        """Copy this record's image_1920 to all linked records in *target_models*.

        *target_models* is a list of model names (e.g. ['res.users', 'hr.employee']).
        Only records whose image_1920 is missing or < 800 bytes are updated.
        """
        self.ensure_one()
        if not self.image_1920 or len(self.image_1920) < 800:
            return

        users, employees, partners = self._get_linked_user_employee_partner()
        targets = []
        if 'res.users' in target_models:
            targets += [r for r in users if r != self]
        if 'hr.employee' in target_models:
            targets += [r for r in employees if r != self]
        if 'res.partner' in target_models:
            targets += [r for r in partners if r != self]

        for rec in targets:
            if not rec.image_1920 or len(rec.image_1920) < 800:
                rec.image_1920 = self.image_1920


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'idphoto.sync.mixin']

    def sync_id_photo_to_user(self):
        """Copy this partner's image to the linked user record."""
        self._sync_image_to_linked(['res.users'])

    def sync_id_photo_to_employee(self):
        """Copy this partner's image to the linked employee record(s)."""
        self._sync_image_to_linked(['hr.employee'])


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'idphoto.sync.mixin']

    def sync_id_photo_to_user(self):
        """Copy this employee's image to the linked user record."""
        self._sync_image_to_linked(['res.users'])

    def sync_id_photo_to_partner(self):
        """Copy this employee's image to the linked partner (address) record."""
        self._sync_image_to_linked(['res.partner'])


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users', 'idphoto.sync.mixin']

    def sync_id_photo_to_employee(self):
        """Copy this user's image to the linked employee record."""
        self._sync_image_to_linked(['hr.employee'])

    def sync_id_photo_to_partner(self):
        """Copy this user's image to the linked partner record."""
        self._sync_image_to_linked(['res.partner'])

