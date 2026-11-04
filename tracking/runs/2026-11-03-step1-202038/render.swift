import AppKit
import PDFKit
import Foundation
let args = CommandLine.arguments
for path in args.dropFirst() {
 guard let doc = PDFDocument(url: URL(fileURLWithPath: path)) else { fatalError("Cannot open PDF") }
 for index in 0..<doc.pageCount {
  let page = doc.page(at: index)!
  let size = page.bounds(for: .mediaBox).size
  let image = page.thumbnail(of: NSSize(width: size.width * 1.5, height: size.height * 1.5), for: .mediaBox)
  let rep = NSBitmapImageRep(data: image.tiffRepresentation!)!
  let data = rep.representation(using: .png, properties: [:])!
  let stem = URL(fileURLWithPath: path).deletingPathExtension().lastPathComponent
  let output = URL(fileURLWithPath: "tracking/runs/2026-11-03-step1-202038/" + stem + "__page" + String(index+1) + ".png")
  try data.write(to: output)
  print(output.path)
 }
}
