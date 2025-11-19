/** @odoo-module */

import {CRMLeadMapArchParser} from "./crm_lead_map_arch_parser.esm";
import {CRMLeadMapController} from "./crm_lead_map_controller.esm";
import {CRMLeadMapModel} from "./crm_lead_map_model.esm";
import {CRMLeadMapRenderer} from "./crm_lead_map_renderer.esm";
import {registry} from "@web/core/registry";

export const CRMLeadMapView = {
    type: "CRMLeadMapView",
    display_name: "Map",
    icon: "fa fa-map",
    multiRecord: true,
    Controller: CRMLeadMapController,
    ArchParser: CRMLeadMapArchParser,
    Model: CRMLeadMapModel,
    Renderer: CRMLeadMapRenderer,

    props(genericProps, view) {
        const {ArchParser} = view;
        const {arch} = genericProps;
        const archInfo = new ArchParser().parse(arch);

        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            archInfo,
        };
    },
};

registry.category("views").add("CRMLeadMapView", CRMLeadMapView);
