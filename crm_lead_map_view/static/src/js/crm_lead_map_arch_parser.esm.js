/** @odoo-module */

export class CRMLeadMapArchParser {
    parse(arch) {
        const text = arch.getAttribute("text");
        const latitude = arch.getAttribute("latitude");
        const longitude = arch.getAttribute("longitude");
        return {
            text,
            latitude,
            longitude,
        };
    }
}
