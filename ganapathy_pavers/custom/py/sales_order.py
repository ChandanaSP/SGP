from codecs import ignore_errors
import site
import frappe
import json
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist()
def get_item_value(doctype):
    res={
        'item_name':frappe.get_value('Item',doctype,'item_name'),
        'description':frappe.get_value('Item',doctype,'description'),
        'uom':frappe.get_value('Item',doctype,'sales_uom')
    }
    return res
    
@frappe.whitelist()
def create_site(doc):
    doc=json.loads(doc)
    supervisor=doc.get('supervisor_name') if('supervisor_name' in doc) else ''
    pavers=[{
            'item':row['item'],
            'required_area':row['required_area'],
            'area_per_bundle':row['area_per_bundle'],
            'number_of_bundle':row['number_of_bundle'],
            'allocated_paver_area':row['allocated_paver_area'],
            'rate':row['rate'],
            'amount':row['amount'],
            'work': doc['work'],
            'sales_order':doc['name']
            } for row in doc['pavers']]
    raw_material=[{
            'item':row['item'],
            'qty':row['qty'],
            'uom':row['uom'],
            'rate':row['rate'],
            'amount':row['amount'],
            'sales_order':doc['name']
            } for row in doc['raw_materials']]
    site_work=frappe.get_doc('Project',doc['site_work'])
    total_area=0
    completed_area=0
    for item in (site_work.get('item_details') or []):
        total_area+=item.required_area
    for item in pavers:
        total_area+=item['required_area']
    for item in (site_work.get('job_worker') or []):
        total_area+=item.sqft_allocated
    
    site_work.update({
        'customer': doc['customer'] or '',
        'supervisor_name': supervisor,
        'item_details': (site_work.get('item_details') or []) +pavers,
        'raw_material': (site_work.get('raw_material') or []) + raw_material,
        'total_required_area': total_area,
        'total_completed_area': completed_area,
        'completed': (completed_area/total_area)*100
    })
    if(doc['is_multi_customer']):
        sw_cust=[cus.customer for cus in (site_work.get('customer_name') or [] )]
        customer=[]
        for cust in doc['customers_name']:
            if(cust['customer'] not in sw_cust):
                customer.append({'customer':cust['customer']})
        site_work.update({
            'customer_name': (site_work.get('customer_name') or [] ) + customer
        })
    site_work.save()
    frappe.db.commit()
    return


@frappe.whitelist()
def create_property():
    doc=frappe.new_doc('Property Setter')
    doc.update({
        "doctype_or_field": "DocField",
        "doc_type":"Sales Order",
        "field_name":"customer",
        "property":"reqd",
        "value":0
    })
    doc.save()
    frappe.db.commit()
    return doc.name
   
   
@frappe.whitelist()
def remove_property(prop_name):
    frappe.delete_doc('Property Setter',prop_name)
    frappe.db.commit()


@frappe.whitelist()
def update_temporary_customer(customer, sales_order):
    doc=frappe.get_doc('Sales Order',sales_order)
    frappe.db.set(doc, "customer", customer)

@frappe.whitelist()
def get_customer_list(sales_order):
    doc=frappe.get_doc('Sales Order', sales_order)
    customer=[cust.customer for cust in doc.customers_name]
    return '\n'.join(customer)
    
