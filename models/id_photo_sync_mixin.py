from odoo import models

class IDPhotoSyncMixin(models.AbstractModel):
    _name = 'idphoto.sync.mixin'
    _description = 'ID Photo Sync Mixin for User, Employee, Partner'

    def sync_images_between_user_employee_partner(self):
        """
        Syncs image_1920 between linked res.users, hr.employee, and res.partner records.
        Whichever record has an image will share it with the others that have none.
        Updates all linked records, not just the first one.
        """
        for record in self:
            user_recs = self.env['res.users']
            partner_recs = self.env['res.partner']
            employee_recs = self.env['hr.employee']

            # Identify starting record type
            if record._name == 'res.users':
                user_recs |= record
                partner_recs |= record.partner_id
                employee_recs |= record.employee_id

            elif record._name == 'hr.employee':
                employee_recs |= record
                user_recs |= record.user_id
                if record.address_home_id:
                    partner_recs |= record.address_id

            elif record._name == 'res.partner':
                partner_recs |= record
                user_recs |= record.user_ids
                if hasattr(record, 'employee_ids'):
                    employee_recs |= record.employee_ids

            # Collect all records in a list (not a recordset) to handle different models
            all_recs = list(user_recs) + list(partner_recs) + list(employee_recs)

            # Find first available image
            image_data = False
            for rec in all_recs:
                if rec.image_1920:
                    image_data = rec.image_1920
                    break

            # Apply to all without image
            if image_data:
                for rec in all_recs:
                    if not rec.image_1920:
                        rec.image_1920 = image_data

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = ['res.partner', 'idphoto.sync.mixin']  

class HrEmployee(models.Model):
    _name = 'hr.employee'
    _inherit = ['hr.employee', 'idphoto.sync.mixin']

class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users', 'idphoto.sync.mixin']

