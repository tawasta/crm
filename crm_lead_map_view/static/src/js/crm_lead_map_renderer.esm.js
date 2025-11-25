/** @odoo-module */

import {Component, onMounted} from "@odoo/owl";

export class CRMLeadMapRenderer extends Component {
    setup() {
        onMounted(async () => {
            // eslint-disable-next-line
            this.map = L.map("crm_lead_map").setView(
                [this.props.company_latitude, this.props.company_longitude],
                13
            );
            // eslint-disable-next-line
            L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 19,
                attribution:
                    "&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>",
            }).addTo(this.map);
            this.props.records.forEach((record) => {
                const text =
                    record.text +
                    " <a href='https://www.google.com/maps?z=15&q=" +
                    record.latitude +
                    "," +
                    record.longitude +
                    "' target='_blank'>Google Maps</a>";
                // eslint-disable-next-line
                L.marker([record.latitude, record.longitude])
                    .bindPopup(text)
                    .addTo(this.map);
            });
        });
    }
}

CRMLeadMapRenderer.template = "crm_lead_map_view.Renderer";
