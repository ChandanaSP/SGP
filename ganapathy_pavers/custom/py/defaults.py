import frappe

@frappe.whitelist()
def create_designation(self, event):
    doc=frappe.new_doc('Designation')
    doc.update({
        'doctype': 'Designation',
        'designation_name': 'Job Worker'
    })
    doc.save()
    frappe.db.commit
    doc=frappe.new_doc('Designation')
    doc.update({
        'doctype': 'Designation',
        'designation_name': 'Operator'
    })
    doc.save()
    frappe.db.commit