/** @odoo-module */

import {Component, onMounted, onRendered, onWillUpdateProps} from "@odoo/owl";

export class CRMLeadMapRenderer extends Component {
    async render() {
        if (this.markers !== undefined) {
            this.markers.forEach((marker) => {
                marker.removeFrom(this.map);
            });
            this.markers = [];
            this.props.records.forEach((record) => {
                const text =
                    "<a target='_blank' href='/web#id=" +
                    record.lead_id +
                    "&model=crm.lead'>" +
                    record.lead_name +
                    "</a></br></br>" +
                    "<a target='_blank' href='/web#id=" +
                    record.partner_id +
                    "&model=res.partner'>" +
                    record.partner_name +
                    "</a></br></br>" +
                    "<a target='_blank' href='https://www.google.com/maps?z=15&q=" +
                    record.latitude +
                    "," +
                    record.longitude +
                    "'>Google Maps</a>";
                // eslint-disable-next-line
                let marker = L.marker([record.latitude, record.longitude]);
                marker.bindPopup(text);
                marker.addTo(this.map);
                this.markers.push(marker);
            });
        }
    }

    setup() {
        onMounted(async () => {
            // eslint-disable-next-line
            this.map = L.map("crm_lead_map").setView(
                [
                    this.props.company_location.latitude,
                    this.props.company_location.longitude,
                ],
                13
            );
            // eslint-disable-next-line
            this.tileLayer = L.tileLayer(
                "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                {
                    maxZoom: 19,
                    attribution:
                        "&copy; <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a>",
                }
            );
            this.map.addLayer(this.tileLayer);
            this.markers = [];
            this.render();
        });
        onRendered(async () => {
            await this.render();
        });
    }
}

CRMLeadMapRenderer.template = "crm_lead_map_view.Renderer";
