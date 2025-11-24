/** @odoo-module */

import {KeepLast} from "@web/core/utils/concurrency";
import {session} from "@web/session";

export class CRMLeadMapModel {
    constructor(orm, rpc, action, resModel, searchModel, fields, archInfo, domain) {
        this.orm = orm;
        this.rpc = rpc;
        this.action = action;
        this.resModel = resModel;
        this.searchModel = searchModel;
        const {latitude, longitude} = archInfo;
        this.latitude = latitude;
        this.longitude = longitude;
        this.fields = fields;
        this.domain = domain;
        this.keepLast = new KeepLast();
    }

    getSpecification() {
        const fields = {};
        fields.id = {};
        fields.name = {};
        if (this.latitude !== undefined) {
            fields[this.latitude] = {};
        }
        if (this.longitude !== undefined) {
            fields[this.longitude] = {};
        }
        fields.partner_id = {};
        return fields;
    }

    async load() {
        const company_id = session.user_companies.current_company;
        var company_result = await this.orm.webSearchRead(
            "res.company",
            [["id", "in", [company_id]]],
            {
                specification: {
                    name: {},
                    company_latitude: {},
                    company_longitude: {},
                },
            }
        );
        if (company_result.length < 1) {
            // No company found center the map to Tampere
            this.company_location = {
                latitude: 61.49911,
                longitude: 23.78712,
            };
        } else {
            this.company_location = {
                latitude: company_result.records[0].company_latitude,
                longitude: company_result.records[0].company_longitude,
            };
        }

        var result = await this.orm.webSearchRead(
            this.resModel,
            this.searchModel._domain,
            {
                specification: this.getSpecification(),
            }
        );

        const partner_ids = $.map(result.records, function(record) {
            return record.partner_id;
        }).filter(function(item) {
            return item;
        });

        var partner_result = await this.orm.webSearchRead(
            "res.partner",
            [["id", "in", partner_ids]],
            {
                specification: {
                    name: {},
                },
            }
        );

        this.records = [];

        result.records.forEach((record) => {
            var marker = {
                lead_name: "",
                lead_id: 0,
                partner_name: "",
                partner_id: 0,
                latitude: 0,
                longitude: 0,
            };
            marker.lead_name = record.name;
            marker.lead_id = record.id;
            partner_result.records.forEach((partner) => {
                if (partner.id == record.partner_id) {
                    marker.partner_id = record.partner_id;
                    marker.partner_name = partner.name;
                }
            });
            if (this.latitude !== undefined) {
                marker.latitude = record[this.latitude];
            }
            if (this.longitude !== undefined) {
                marker.longitude = record[this.longitude];
            }
            this.records.push(marker);
        });
    }
}
