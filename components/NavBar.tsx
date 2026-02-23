import Link from "next/link";

const links = [
  { href: "/", label: "Home" },
  { href: "/dashboard", label: "Transparency Dashboard" },
  { href: "/library", label: "Humanity Library" },
  { href: "/ai-hub", label: "AI & Evolution" },
  { href: "/manifesto", label: "2026 Horizon" },
  { href: "/forum", label: "Unity Forum" }
];

export function NavBar() {
  return (
    <header className="sticky top-0 z-20 border-b border-sky-200/80 bg-white/85 backdrop-blur">
      <nav className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-3 px-4 py-3">
        <Link href="/" className="font-semibold tracking-wide text-sky-700">
          HORIZON 2026
        </Link>
        <ul className="flex flex-wrap gap-3 text-sm text-slate-700">
          {links.map((link) => (
            <li key={link.href}>
              <Link className="transition hover:text-sky-700" href={link.href}>
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
}
