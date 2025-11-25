/** @odoo-module */

import {KeepLast} from "@web/core/utils/concurrency";
import {session} from "@web/session";

export class CRMLeadMapModel {
    constructor(orm, rpc, resModel, searchModel, fields, archInfo, domain) {
        this.orm = orm;
        this.rpc = rpc;
        this.resModel = resModel;
        this.searchModel = searchModel;
        this.fields = fields;
        this.domain = domain;
        this.keepLast = new KeepLast();
        this.company_latitude = 0;
        this.company_longitude = 0;
    }

    async load() {
        const company_id = session.user_companies.current_company;
        var company_result = await this.orm.webSearchRead(
            "res.company",
            [["id", "in", [company_id]]],
            {
                specification: {
                    name: {},
                    partner_id: {},
                },
            }
        );
        const company_partner_id = company_result.records[0].partner_id;
        var company_partner_result = await this.orm.webSearchRead(
            "res.partner",
            [["id", "=", company_partner_id]],
            {
                specification: {
                    name: {},
                    partner_latitude: {},
                    partner_longitude: {},
                },
            }
        );
        if (company_partner_result.length < 1) {
            // No company found center the map to Tampere
            this.company_latitude = 61.49911;
            this.company_longitude = 23.78712;
        } else {
            this.company_latitude = company_partner_result.records[0].partner_latitude;
            this.company_longitude =
                company_partner_result.records[0].partner_longitude;
        }

        var result = await this.orm.webSearchRead(
            this.resModel,
            this.searchModel._domain,
            {
                specification: {
                    id: {},
                    name: {},
                    partner_id: {},
                },
            }
        );

        const partner_ids = $.map(result.records, function (record) {
            return record.partner_id;
        }).filter(function (item) {
            return item;
        });

        var partner_result = await this.orm.webSearchRead(
            "res.partner",
            [["id", "in", partner_ids]],
            {
                specification: {
                    name: {},
                    partner_latitude: {},
                    partner_longitude: {},
                },
            }
        );

        this.records = [];

        result.records.forEach((record) => {
            var marker = {
                lead_name: record.name,
                lead_id: record.id,
                partner_name: "",
                partner_id: 0,
                latitude: 0,
                longitude: 0,
            };
            marker.lead_name = record.name;
            marker.lead_id = record.id;
            partner_result.records.forEach((partner) => {
                if (partner.id === record.partner_id) {
                    marker.partner_id = record.partner_id;
                    marker.partner_name = partner.name;
                    marker.latitude = partner.partner_latitude;
                    marker.longitude = partner.partner_longitude;
                }
            });
            this.records.push(marker);
        });
    }
}
