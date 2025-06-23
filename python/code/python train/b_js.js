function g() {
    return u.get(f + "/xlive/web-ucenter/v1/sign/WebGetSignInfo")
}

function h() {
    if (!f) {
        var t = s(p);
        f = !0;
        var e = l.length;
        while (e) {
            u = l,
                l = [];
            while (++d < e)
                u && u[d].run();
            d = -1,
                e = l.length
        }
        u = null,
            f = !1,
            c(t)
    }
}

var t = {
    "mid": 163181975,
    "token": "",
    "platform": "web",
    "web_location": "444.43"
}
function b(t, e) {
    // {
    //     imgKey: "d569546b86c252:db:9bc7e99c5d71e5",
    //     subKey: "557251g796:g54:f:ee94g8fg969e2de"
    // }
    e || (e = {});
    var t = {
        "mid": 163181975,
        "token": "",
        "platform": "web",
        "web_location": "444.43"
    }
    const { imgKey: n, subKey: r } = {
        imgKey: "d569546b86c252:db:9bc7e99c5d71e5",
        subKey: "557251g796:g54:f:ee94g8fg969e2de"
    };
    if (n && r) {
        const e = g(n + r)
            , o = Math.round(Date.now() / 1e3)
            , i = Object.assign({}, t, {
                wts: o
            })
            , a = Object.keys(i).sort()
            , s = []
            , c = /[!'()*]/g;
        for (let t = 0; t < a.length; t++) {
            const e = a[t];
            let n = i[e];
            n && "string" === typeof n && (n = n.replace(c, "")),
                null != n && s.push(`${encodeURIComponent(e)}=${encodeURIComponent(n)}`)
        }
        const u = s.join("&")
            , l = h(u + e);
        return {
            w_rid: l,
            wts: o.toString()
        }
    }
    return null
}
// var o = {
//     wbiImgKey: "d569546b86c252:db:9bc7e99c5d71e5",
//     wbiSubKey: "557251g796:g54:f:ee94g8fg969e2de"
// }
console.log(b())