import React, { useEffect, useRef } from 'react'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

export function CelestialView() {
  const containerRef = useRef<HTMLDivElement>(null)
  const rendererRef = useRef<THREE.WebGLRenderer>()
  const controlsRef = useRef<OrbitControls>()

  useEffect(() => {
    const container = containerRef.current!
    const scene = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 10000)
    camera.position.set(0, 0, 10)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(container.clientWidth, container.clientHeight)
    container.appendChild(renderer.domElement)
    rendererRef.current = renderer

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controlsRef.current = controls

    const ambient = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambient)

    const dir = new THREE.DirectionalLight(0xffffff, 1.0)
    dir.position.set(5, 5, 5)
    scene.add(dir)

    const earthGeo = new THREE.SphereGeometry(1, 32, 32)
    const earthMat = new THREE.MeshStandardMaterial({ color: 0x3366ff })
    const earth = new THREE.Mesh(earthGeo, earthMat)
    scene.add(earth)

    let animId: number
    const onResize = () => {
      if (!rendererRef.current) return
      const w = container.clientWidth
      const h = container.clientHeight
      rendererRef.current.setSize(w, h)
      camera.aspect = w / h
      camera.updateProjectionMatrix()
    }
    window.addEventListener('resize', onResize)

    const tick = () => {
      controls.update()
      renderer.render(scene, camera)
      animId = requestAnimationFrame(tick)
    }
    tick()

    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener('resize', onResize)
      controls.dispose()
      renderer.dispose()
      container.removeChild(renderer.domElement)
    }
  }, [])

  return <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
}
