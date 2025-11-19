/** @odoo-module */

import {KeepLast} from "@web/core/utils/concurrency";
import {session} from "@web/session";

export class CRMLeadMapModel {
    constructor(orm, rpc, resModel, fields, archInfo, domain) {
        this.orm = orm;
        this.rpc = rpc;
        this.resModel = resModel;
        const {text, latitude, longitude} = archInfo;
        this.text = text;
        this.latitude = latitude;
        this.longitude = longitude;
        this.fields = fields;
        this.domain = domain;
        this.keepLast = new KeepLast();
    }

    getSpecification() {
        // Which fields are used for text, latitude and longitude
        // are dynamic and passed from the view to map_arch_parser to
        // here
        var fields = {};
        if (this.text !== undefined) {
            fields[this.text] = {};
        }
        if (this.latitude !== undefined) {
            fields[this.latitude] = {};
        }
        if (this.longitude !== undefined) {
            fields[this.longitude] = {};
        }
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
        console.log(company_result);
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

        var result = await this.orm.webSearchRead(this.resModel, [], {
            specification: this.getSpecification(),
        });

        this.records = [];

        result.records.forEach((record) => {
            var marker = {text: "", latitude: 0, longitude: 0};
            if (this.text !== undefined) {
                marker.text = record[this.text];
            }
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
