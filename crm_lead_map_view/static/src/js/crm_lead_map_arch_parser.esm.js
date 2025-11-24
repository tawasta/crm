/** @odoo-module */

export class CRMLeadMapArchParser {
    // eslint-disable-next-line
    parse(arch, fields) {
        const latitude = arch.getAttribute("latitude");
        const longitude = arch.getAttribute("longitude");
        return {
            latitude,
            longitude,
        };
    }
}
