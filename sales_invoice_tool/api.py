from __future__ import unicode_literals
import frappe
from frappe.utils import cint, get_gravatar, format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day,flt,nowdate
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.utils.user import get_system_managers
import frappe.permissions
import frappe.share
from frappe.model.mapper import get_mapped_doc



@frappe.whitelist()
def submitInvoice(from_date,to_date):
	invoice_list=frappe.get_all("Sales Invoice",filters=[["Sales Invoice","posting_date","Between",[from_date,to_date]],["Sales Invoice","status","=","Draft"]],fields=["name"])
	if invoice_list:
		frappe.enqueue(submitAllInvoice, timeout=120, invoice_list=invoice_list)
	else:
		frappe.msgprint("No Any Draft Invoice Found")


@frappe.whitelist()
def submitAllInvoice(invoice_list):
	count=0
	for row in invoice_list:
		doc=frappe.get_doc("Sales Invoice",row.name)
		doc.submit()
		count += 1
	frappe.msgprint(str(count)+" Sales Invoice Submitted")
		
		
