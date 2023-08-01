/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.up = function (knex) {
    return Promise.all([
        knex.schema.table("user", function (table) {
            table.string("sex").defaultTo("girl"); // 增加 sex 字段，并设置默认值
        }),
        knex.schema.table("user", function (table) {
            table.string("gender").defaultTo("mzzi"); // 增加 gender 字段，并设置默认值
        })
    ])
};

/**
 * @param { import("knex").Knex } knex
 * @returns { Promise<void> }
 */
exports.down = function (knex) {
    return Promise.all([
        knex.schema.table("user", function (table) {
            table.dropColumn("sex");
        }),
        knex.schema.table("user", function (table) {
            table.dropColumn("gender");
        })
    ])
};
