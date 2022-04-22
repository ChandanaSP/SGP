frappe.ui.form.on('Timesheet', {
    on_submit: function(frm) {
            frappe.db.get_value('Workstation', {'name':cur_frm.doc.workstation}, '_assign', function(r) {
                cur_frm.assign_to.add();
                cur_frm.assign_to.assign_to.dialog.set_values({assign_to:r._assign});
                setTimeout(() => {
                    frm.assign_to.assign_to.dialog.primary_action();
                }, 100);
			});
        },
});
var exists=[];
frappe.ui.form.on('Timesheet Detail',{
    total_production_pavers:function(frm,cdt,cdn){
        let row=locals[cdt][cdn]
        if(exists.includes(row.item)){
            var qty_table=frm.doc.item_produced_quantity
            for (let data in qty_table){
                if(row.item==qty_table[data].item){
                    let existing_qty=qty_table[data].quantity_produced
                    frappe.model.set_value(qty_table[data].doctype,qty_table[data].name,'quantity_produced',existing_qty+row.total_production_pavers)
                    cur_frm.refresh_field("item_produced_quantity")
                }
            }
        }
        else{
            exists.push(row.item)
            var child = cur_frm.add_child("item_produced_quantity");
            frappe.model.set_value(child.doctype, child.name, "item", row.item)     
            frappe.model.set_value(child.doctype, child.name, "quantity_produced",row.total_production_pavers)
            cur_frm.refresh_field("item_produced_quantity")
        }
    }

})
