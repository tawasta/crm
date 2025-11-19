/** @odoo-module */

import {Component, onWillStart, useState} from "@odoo/owl";
import {Layout} from "@web/search/layout";
import {SearchBar} from "@web/search/search_bar/search_bar";
import {useService} from "@web/core/utils/hooks";

export class CRMLeadMapController extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.model = useState(
            new this.props.Model(
                this.orm,
                this.rpc,
                this.props.resModel,
                this.props.fields,
                this.props.archInfo,
                this.props.domain
            )
        );

        onWillStart(async () => {
            await this.model.load();
        });
    }
}

CRMLeadMapController.components = {Layout, SearchBar};
CRMLeadMapController.template = "crm_lead_map_view.View";
