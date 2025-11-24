/** @odoo-module */

import {Component, onWillStart, onWillUpdateProps, useState} from "@odoo/owl";
import {Layout} from "@web/search/layout";
import {SearchBar} from "@web/search/search_bar/search_bar";
import {useService} from "@web/core/utils/hooks";

export class CRMLeadMapController extends Component {
    setup() {
        this.dataSearch = [];
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.action = useService("action");
        this.ui = useService("ui");
        this.model = useState(
            new this.props.Model(
                this.orm,
                this.rpc,
                this.action,
                this.props.resModel,
                this.env.searchModel,
                this.props.fields,
                this.props.archInfo,
                this.props.domain
            )
        );

        onWillStart(async () => {
            await this.model.load();
        });

        onWillUpdateProps(async () => {
            await this.model.load();
        });
    }
}

CRMLeadMapController.components = {Layout, SearchBar};
CRMLeadMapController.template = "crm_lead_map_view.View";
