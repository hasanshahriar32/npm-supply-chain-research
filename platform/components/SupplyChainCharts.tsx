import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

type Analytics = {
  recordCount: number;
  blastRadiusDistribution: Array<{ bucket: string; packages: number }>;
  topBlastRadius: Array<{ packageName: string; blastRadius: number; transitiveDependents: number }>;
  topAttackerRoi: Array<{ packageName: string; attackerRoi: number; blastRadius: number }>;
};

const chartInk = "#11110f";
const chartRust = "#d25831";
const chartAcid = "#b9d75c";

export function SupplyChainCharts({ data }: { data: Analytics }) {
  return <section className="chart-suite">
    <div className="chart-heading"><div><span className="eyebrow">Observed metric distribution</span><h2>Blast radius across {data.recordCount.toLocaleString()} package metrics</h2></div><p>These charts visualize the committed deterministic metrics snapshot. They are not model-performance claims or exploitation predictions.</p></div>
    <div className="chart-grid">
      <article className="chart-card"><div className="chart-card-header"><h3>Blast-radius frequency</h3><span>Packages by score</span></div><div className="chart-canvas"><ResponsiveContainer width="100%" height={250}><BarChart data={data.blastRadiusDistribution} margin={{ top: 12, right: 8, left: -22, bottom: 0 }}><CartesianGrid vertical={false} stroke="#d8d0c3" /><XAxis dataKey="bucket" tickLine={false} axisLine={false} tick={{ fill: "#6d6a63", fontSize: 10 }} /><YAxis tickLine={false} axisLine={false} tick={{ fill: "#6d6a63", fontSize: 10 }} /><Tooltip cursor={{ fill: "#eee8dd" }} contentStyle={{ border: "1px solid #11110f", borderRadius: 0, background: "#fffdf7", fontSize: 12 }} /><Bar dataKey="packages" radius={0}>{data.blastRadiusDistribution.map((entry, index) => <Cell key={entry.bucket} fill={index === 2 ? chartRust : chartInk} />)}</Bar></BarChart></ResponsiveContainer></div></article>
      <article className="chart-card"><div className="chart-card-header"><h3>Highest observed reach</h3><span>Transitive dependents</span></div><div className="chart-canvas"><ResponsiveContainer width="100%" height={250}><BarChart data={data.topBlastRadius.slice(0, 7)} layout="vertical" margin={{ top: 6, right: 10, left: 10, bottom: 0 }}><CartesianGrid horizontal={false} stroke="#d8d0c3" /><XAxis type="number" hide /><YAxis type="category" dataKey="packageName" width={88} tickLine={false} axisLine={false} tick={{ fill: "#6d6a63", fontSize: 10 }} /><Tooltip cursor={{ fill: "#eee8dd" }} contentStyle={{ border: "1px solid #11110f", borderRadius: 0, background: "#fffdf7", fontSize: 12 }} /><Bar dataKey="transitiveDependents" fill={chartAcid} /></BarChart></ResponsiveContainer></div></article>
    </div>
    <article className="chart-card chart-card-wide"><div className="chart-card-header"><h3>Top structural-risk signals</h3><span>Attacker-ROI proxy with blast-radius context</span></div><div className="chart-canvas"><ResponsiveContainer width="100%" height={280}><BarChart data={data.topAttackerRoi} margin={{ top: 12, right: 8, left: -22, bottom: 48 }}><CartesianGrid vertical={false} stroke="#d8d0c3" /><XAxis dataKey="packageName" interval={0} angle={-36} textAnchor="end" height={64} tickLine={false} axisLine={false} tick={{ fill: "#6d6a63", fontSize: 10 }} /><YAxis tickLine={false} axisLine={false} tick={{ fill: "#6d6a63", fontSize: 10 }} /><Tooltip cursor={{ fill: "#eee8dd" }} contentStyle={{ border: "1px solid #11110f", borderRadius: 0, background: "#fffdf7", fontSize: 12 }} /><Bar dataKey="attackerRoi" fill={chartRust} /></BarChart></ResponsiveContainer></div></article>
  </section>;
}
