// Copyright (c) 2017, sahil and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sync Configuration', {
	refresh: function(frm) {
		if(!frm.doc.__islocal && frm.doc.is_sync && frm.doc.gmail_id){
			cur_frm.add_custom_button(__("Sync Calender"), function(){
				var doc = cur_frm.doc;
				console.log("sahil is here");
				return frappe.call({
					freeze:true,
					freeze_message:"Syncing Google Calender Events",
					method:"gcal.gcal_sync.doctype.sync_configuration.sync_configuration.sync_calender",
					callback: function(r){
						console.log(r);
						if (r.message)
							if(r.message.url)
								window.location.replace(r.message.url);
							if(r.message.is_synced)
								frappe.msgprint("Google Calendar Events synced sucessfully")
						else
							frappe.msgprint("Error occured please try after some time")
					}
				});
			}).addClass("btn-primary");
		} else if(!frm.doc.is_sync){
			frappe.msgprint("Please Check Sync Google Calendar field for Sync Google Calender")
		}
	}
});

/*
cur_frm.cscript.validate = function(){
	if(cur_frm.doc.is_sync)
		hide_gcal_fields(cur_frm.doc.is_sync);
	else
		hide_gcal_fields(0);
}

cur_frm.cscript.is_sync = function(doc){
	hide_gcal_fields(doc.is_sync)
}

hide_gcal_fields = function(is_sync){
	cur_frm.set_df_property("section_break_2", "hidden", is_sync == 0);
}
*/
