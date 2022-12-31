odoo.define('dung.fix_column_pivot', function (require) {
    "use strict";
    console.log('ok men a 123')
    var PivotView = require('web.PivotView');
    var PivotModel = require('web.PivotModel');
    PivotView.include({
        init: function () {
            this._super.apply(this, arguments);
            this._super.apply(this, arguments);
            let cssTable = 'table {position: relative;}'
            let cssOpened = '.o_pivot_header_cell_opened {position: sticky;left: 0px;z-index: 10 !important;} .o_pivot_header_cell_closed{position: sticky;left: 0px;z-index: 10 !important;}'
            let cssThead = 'thead {position: sticky;top: 0px;z-index: 30;}'
            let cssMeasure = '.o_pivot_measure_row {z-index: 30 !important;}'
            let cssSpace = 'table > thead > tr > th:first-child {position: sticky;left: 0px;top: 0px;z-index: 40;}'
            let head = document.head || document.getElementsByTagName('head')[0]
            let style = document.createElement('style');

            head.appendChild(style);

            style.type = 'text/css';
            if (style.styleSheet) {
                // This is required for IE8 and below.
                style.styleSheet.cssText = cssTable + cssOpened + cssThead + cssSpace + cssMeasure;
            } else {
                style.appendChild(document.createTextNode(cssTable + cssOpened + cssThead + cssSpace + cssMeasure));
            }
        },
    });

    PivotModel.include({
        _getSelectionGroupBy: function (groupBys) {
            let fields = this._super.apply(this, arguments);
            if (this.loadParams.context['appearance_column']) {
                let found;
                let all_field_appear = this.loadParams.context['appearance_column'].concat(
                    this.loadParams.colGroupBys, this.loadParams.rowGroupBys, this.loadParams.measures)
                for (let i = 0; i < fields.length; i++) {
                    found = all_field_appear.findIndex(function (item) {
                        return item == fields[i].name;
                    });
                    if (found == -1) {
                        fields.splice(i, 1);
                        i--;
                    }
                }
            }
            //        console.log('_getSelectionGroupBy fields: ',fields)
            return fields;
        },

        _getTableHeaders: function () {
            let headers = this._super.apply(this, arguments);
            let measure_header = headers[headers.length - 1]
            if (this.loadParams.context['invisible_measures']) {
                let all_field_invisible = this.loadParams.context['invisible_measures']
                let found;
                let reduce_count = 0
                //        xoa cac cot trong header
                for (let i = 0; i < all_field_invisible.length; i++) {
                    found = this.loadParams.measures.findIndex(function (item) {
                        return item == all_field_invisible[i];
                    });

                    if (found != -1) {
                        reduce_count += 1
                    }
                }
                let data;
                for (let i = 1; i < headers.length - 1; i++) {
                    data = headers[i]
                    for (let j = 0; j < data.length; j++) {
                        data[j].width -= reduce_count
                    }
                }

                //        xoa cac meansure
                for (let i = 0; i < measure_header.length; i++) {
                    found = all_field_invisible.findIndex(function (item) {
                        return item == measure_header[i].measure;
                    });
                    if (found != -1) {
                        headers[headers.length - 1].splice(i, 1);
                        i--;
                    }
                }
            }

            //        console.log('headers meansure: ',headers)
            return headers;
        },
    });
});